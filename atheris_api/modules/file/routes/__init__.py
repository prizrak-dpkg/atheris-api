# FastAPI imports
from fastapi import APIRouter

# Own imports
from .file import router as file_router

router = APIRouter()

router.include_router(file_router)
