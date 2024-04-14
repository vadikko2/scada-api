import fastapi

from presentation.routes.subscriptions import tech_nests

__all__ = ("router",)


router = fastapi.APIRouter(tags=["Subscriptions"])
router.include_router(tech_nests.router)
