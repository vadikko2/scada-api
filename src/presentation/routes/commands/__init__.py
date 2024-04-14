import fastapi

from presentation.routes.commands import holders, indicators, tech_nests

__all__ = ("router",)


router = fastapi.APIRouter(tags=["Commands"])
router.include_router(holders.router)
router.include_router(tech_nests.router)
router.include_router(indicators.router)
