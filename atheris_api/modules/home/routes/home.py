# FastAPI
from fastapi import APIRouter

# Own imports
from ..services.home import HomeRequest

router = APIRouter()

router.add_api_route(
    "/product_slide",
    methods=["GET"],
    endpoint=HomeRequest().get_async,
)

router.add_api_route(
    "/product_slide",
    methods=["POST"],
    endpoint=HomeRequest().create_product_slide_async,
)
