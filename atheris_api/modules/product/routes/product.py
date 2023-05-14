# FastAPI
from fastapi import APIRouter

# Own imports
from ..services.product import ProductRequest

router = APIRouter()

router.add_api_route(
    "/track",
    methods=["GET"],
    endpoint=ProductRequest().get_track_async,
)

router.add_api_route(
    "/customer",
    methods=["POST"],
    endpoint=ProductRequest().create_async,
)
