# FastAPI
from fastapi import APIRouter

# Own imports
from ..services.product import ProductRequest

router = APIRouter()

# router.add_api_route(
#     "/product_slide",
#     methods=["GET"],
#     endpoint=HomeRequest().get_async,
# )

router.add_api_route(
    "/customer",
    methods=["POST"],
    endpoint=ProductRequest().create_async,
)
