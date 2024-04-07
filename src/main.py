import fastapi

from infrastructire import settings, orm
from presentation import application
from presentation.routes.queries import holders
from presentation.routes.commands import holders as holder_commands
from presentation.routes.subscriptions import tech_nests as tech_nests_sub
from presentation.routes.events import indicators  as indicators_events

app: fastapi.FastAPI = application.create(
    debug=True,
    command_routers=(holder_commands.router,),
    query_routers=(holders.router,),
    subscription_routers=(tech_nests_sub.router,),
    events_routers=(indicators_events.router,),
    middlewares=[],
    startup_tasks=[orm.start_mappers],
    shutdown_tasks=[],
    global_dependencies=[],
    title=settings.app_name,
    version=settings.version,
)
