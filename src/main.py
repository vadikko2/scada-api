import fastapi

from infrastructire import settings, orm
from presentation import application
from presentation.routes.queries import holders, tech_nests
from presentation.routes.commands import holders as holder_commands

app: fastapi.FastAPI = application.create(
    debug=True,
    command_routers=(holder_commands.router,),
    query_routers=(holders.router, tech_nests.router),
    middlewares=[],
    startup_tasks=[orm.start_mappers],
    shutdown_tasks=[],
    global_dependencies=[],
    title=settings.app_name,
    version=settings.version,
)
