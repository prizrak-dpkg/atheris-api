# FastAPI
from fastapi import APIRouter

# Own imports
from ..services.rating import RatingRequest

router = APIRouter()

router.add_api_route(
    "/rating",
    methods=["GET"],
    endpoint=RatingRequest().get_async,
)

router.add_api_route(
    "/rating",
    methods=["POST"],
    endpoint=RatingRequest().create_rating_async,
)
