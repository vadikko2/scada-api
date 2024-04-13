import asyncio
import functools
import typing

import fastapi
import pydantic
from fastapi import exceptions as fastapi_exceptions
from fastapi import routing
from fastapi.middleware import cors
from fastapi.openapi.utils import get_openapi
from starlette.middleware.base import RequestResponseEndpoint

from domain import exceptions
from presentation.errors import handlers as error_handlers
from presentation.errors import registry
from presentation.middlewares import logging_middleware

__all__ = ("create",)


MiddlewareAlias: typing.TypeAlias = typing.Callable[
    [
        fastapi.Request,
        RequestResponseEndpoint,
        ...,
    ],
    typing.Awaitable[fastapi.Response],
]


def custom_openapi(app: fastapi.FastAPI):
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Scada API specification",
        routes=app.routes,
    )

    # Add WebSocket route to the schema
    for route in app.routes:
        if not isinstance(route, routing.APIWebSocketRoute):
            continue
        openapi_schema["paths"][route.path] = {
            "get": {
                "summary": route.name,
                "responses": {
                    200: {
                        "description": "WebSocket",
                    }
                },
                "tags": [
                    "Subscriptions",
                ],
            }
        }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def settings_cors(app: fastapi.FastAPI):
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create(
    *_,
    command_routers: typing.Iterable[fastapi.APIRouter],
    query_routers: typing.Iterable[fastapi.APIRouter],
    subscription_routers: typing.Iterable[fastapi.APIRouter],
    middlewares: typing.Iterable[MiddlewareAlias] | None = None,
    startup_tasks: typing.Iterable[typing.Callable[[], typing.Coroutine]] | None = None,
    shutdown_tasks: typing.Iterable[typing.Callable[[], typing.Coroutine]] | None = None,
    global_dependencies: typing.Iterable[typing.Callable[[], typing.Awaitable[typing.Any]]] | None = None,
    set_cors: bool = False,
    **kwargs,
) -> fastapi.FastAPI:
    if global_dependencies is None:
        global_dependencies = []
    # Инициализирует приложение FastAPI
    app = fastapi.FastAPI(
        **kwargs,
        dependencies=global_dependencies,
        responses=registry.get_exception_responses(Exception, fastapi_exceptions.RequestValidationError),
    )

    # Include REST API routers
    for router in command_routers:
        app.include_router(router)
    for router in query_routers:
        app.include_router(router)
    for router in subscription_routers:
        app.include_router(router)

    # Расширяет default обработчики ошибок FastAPI
    # Расширяет default обработчики ошибок FastAPI
    app.exception_handler(fastapi_exceptions.RequestValidationError)(
        error_handlers.pydantic_request_validation_errors_handler
    )
    app.exception_handler(pydantic.ValidationError)(error_handlers.pydantic_request_validation_errors_handler)
    app.exception_handler(exceptions.AlreadyExists)(error_handlers.already_exists_handler)
    app.exception_handler(exceptions.NotFound)(error_handlers.not_found_handler)

    if middlewares is None:
        middlewares = []
    for middleware in middlewares:
        app.add_middleware(middleware)

    app.middleware("http")(logging_middleware.LoggingMiddleware())
    app.middleware("https")(logging_middleware.LoggingMiddleware())

    if set_cors:
        settings_cors(app)

    # Инициализирует все startup таски
    if startup_tasks:
        for task in startup_tasks:
            coro = functools.partial(asyncio.create_task, task())
            app.on_event("startup")(coro)

    # Инициализирует все shutdown таски
    if shutdown_tasks:
        for task in shutdown_tasks:
            app.on_event("shutdown")(task)

    # Формируем документацию
    custom_openapi(app=app)

    return app
