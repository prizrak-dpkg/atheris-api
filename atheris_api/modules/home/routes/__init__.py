# FastAPI imports
from fastapi import APIRouter

# Own imports
from .home import router as home_router
from .rating import router as rating_router

router = APIRouter()

router.include_router(home_router, tags=["Home"])
router.include_router(rating_router, tags=["Home"])
