# FastAPI imports
from fastapi import APIRouter

# Own imports
from .product import router as product_router

router = APIRouter()

router.include_router(product_router, tags=["Product"])
