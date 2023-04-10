# FastAPI
from fastapi import APIRouter


# Own imports
from ..services.file import FileRequest

router = APIRouter()

router.add_api_route(
    "/read_slide",
    methods=["GET"],
    endpoint=FileRequest().read_slide_async,
    tags=["Slides"],
)
