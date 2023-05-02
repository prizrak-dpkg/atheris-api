# Uvicorn imports
import uvicorn

# Starlette imports
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

# FastAPI imports
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.requests import Request
from fastapi.responses import JSONResponse

# Beanie imports
from beanie import init_beanie

# Own imports
from config.base_settings import get_settings
from config.beanie import db_session as mongo_db_session
from atheris_api.modules import models, routers


def init_api() -> FastAPI:
    api = FastAPI(
        title="Crab API",
        description="""
        Crab API is an API to manage customers, invoices and advertising campaigns for many shopping malls.

        Versions are handled with 3 numbers, X.Y.Z, and each one indicates a different thing:

            1. The first (X) is known as the main version and indicates the main version of the software. Example: 1.0.0, 3.0.0.
            2. The second (Y) is known as minor version and indicates new features. Example: 1.2.0, 3.3.0
            3. The third (Z) is known as a revision and indicates that a code review has been performed due to a bug. Example: 1.2.2, 3.3.4
        """,
        version="0.1.0",
    )
    api.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().ORIGINS.split(","),
        allow_credentials=False,
        allow_methods=("GET", "POST"),
        allow_headers=("Content-Type", "Authorization", "Host", "User-Agent"),
    )

    @api.on_event("startup")
    async def startup():
        """
        Callback function for the startup event
        """
        mongo_db_session.init()
        await init_beanie(mongo_db_session.get_database, document_models=[*models])
        for router in routers:
            api.include_router(router, prefix="/api")

    @api.on_event("shutdown")
    async def shutdown():
        """
        Callback function for the shutdown event
        """
        ...

    @api.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        errors = []
        for error in exc.errors():
            if len(error["loc"]) > 0:
                errors.append(
                    {"field": error["loc"][len(error["loc"]) - 1], "msg": error["msg"]}
                )
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": errors},
        )

    return api


crab = init_api()


def start():
    """
    Starts the Uvicorn server to run the FastAPI instance
    """
    uvicorn.run("atheris_api.main:crab", host="0.0.0.0", port=8888, reload=True)
