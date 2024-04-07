import fastapi

from infrastructire import orm, settings
from presentation import application
from presentation.routes.commands import holders as holder_commands
from presentation.routes.commands import indicators as indicators_events
from presentation.routes.queries import holders, tech_nests
from presentation.routes.subscriptions import tech_nests as tech_nests_sub

app: fastapi.FastAPI = application.create(
    debug=True,
    command_routers=(
        holder_commands.router,
        indicators_events.router,
    ),
    query_routers=(
        holders.router,
        tech_nests.router,
    ),
    subscription_routers=(tech_nests_sub.router,),
    middlewares=[],
    startup_tasks=[orm.start_mappers],
    shutdown_tasks=[],
    global_dependencies=[],
    title=settings.app_name,
    version=settings.version,
)
