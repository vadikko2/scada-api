import asyncio
import functools
import typing

import fastapi
from starlette.middleware.base import RequestResponseEndpoint

__all__ = ("create",)

from presentation.middlewares import logging_middleware

MiddlewareAlias: typing.TypeAlias = typing.Callable[
    [
        fastapi.Request,
        RequestResponseEndpoint,
        ...,
    ],
    typing.Awaitable[fastapi.Response],
]


def create(
    *_,
    command_routers: typing.Iterable[fastapi.APIRouter],
    query_routers: typing.Iterable[fastapi.APIRouter],
    events_routers: typing.Iterable[fastapi.APIRouter],
    subscription_routers: typing.Iterable[fastapi.APIRouter],
    middlewares: typing.Iterable[MiddlewareAlias] | None = None,
    startup_tasks: typing.Iterable[typing.Callable[[], typing.Coroutine]] | None = None,
    shutdown_tasks: typing.Iterable[typing.Callable[[], typing.Coroutine]] | None = None,
    global_dependencies: typing.Iterable[typing.Callable[[], typing.Awaitable[typing.Any]]] | None = None,
    **kwargs,
) -> fastapi.FastAPI:
    if global_dependencies is None:
        global_dependencies = []
    # Инициализирует приложение FastAPI
    app = fastapi.FastAPI(**kwargs, dependencies=global_dependencies)

    # Include REST API routers
    for router in command_routers:
        app.include_router(router)
    for router in query_routers:
        app.include_router(router)
    for router in subscription_routers:
        app.include_router(router)
    for router in events_routers:
        app.include_router(router)
    # Расширяет default обработчики ошибок FastAPI
    pass

    if middlewares is None:
        middlewares = []
    for middleware in middlewares:
        app.add_middleware(middleware)

    app.middleware("http")(logging_middleware.LoggingMiddleware())

    # Инициализирует все startup таски
    if startup_tasks:
        for task in startup_tasks:
            coro = functools.partial(asyncio.create_task, task())
            app.on_event("startup")(coro)

    # Инициализирует все shutdown таски
    if shutdown_tasks:
        for task in shutdown_tasks:
            app.on_event("shutdown")(task)

    return app
