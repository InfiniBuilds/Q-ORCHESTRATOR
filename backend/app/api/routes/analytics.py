from fastapi import APIRouter

from app.analytics.service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

service = AnalyticsService()


@router.get("/summary")
def get_summary():
    return service.get_summary()
