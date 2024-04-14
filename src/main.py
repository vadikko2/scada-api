import fastapi

from infrastructire import settings
from presentation import application
from presentation.routes import commands, queries, subscriptions

app: fastapi.FastAPI = application.create(
    debug=settings.debug,
    command_routers=(commands.router,),
    query_routers=(queries.router,),
    subscription_routers=(subscriptions.router,),
    middlewares=[],
    startup_tasks=[],
    shutdown_tasks=[],
    global_dependencies=[],
    title=settings.app_name,
    version=settings.version,
    set_cors=True,
)
