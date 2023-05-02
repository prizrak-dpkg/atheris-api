# Python imports
from typing import Dict, List
import json

# Starlette imports
from pydantic import ValidationError
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

# FastAPI imports
from fastapi import Form, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

# Own imports
from atheris_api.modules.file.services.file import FileRequest
from atheris_api.modules.home.models.home import ProductSlideModel
from atheris_api.modules.home.schemas.home import (
    ProductSlideSchema,
    ProductSlideListSchema,
)
from atheris_api.utils.paginate import PaginatedListSchema, PaginatedRequest


class HomeRequest(PaginatedRequest):
    async def get_async(
        self, limit: int = 10, page: int = 1, title: str = ""
    ) -> ProductSlideListSchema:
        results: List[ProductSlideSchema] = []
        product_slides: List[ProductSlideModel]
        page_information: PaginatedListSchema
        page_information, product_slides = await self.get_query_by_field_async(
            ProductSlideModel, "title", title, limit, page
        )
        for product_slide in product_slides:
            results.append(
                ProductSlideSchema(
                    id=product_slide.id,
                    title=product_slide.title,
                    desc=product_slide.desc,
                    banner=product_slide.banner,
                    slideInfo=product_slide.slideInfo,
                )
            )
        return ProductSlideListSchema(
            total=page_information.total,
            num_pages=page_information.num_pages,
            current_page=page_information.current_page,
            per_page=page_information.per_page,
            results=results,
        )

    async def create_product_slide_async(
        self,
        title: str = Form(
            ..., description="Title of the product slide (e.g. Camisetas)"
        ),
        desc: str = Form(
            ...,
            description="Description of the product slide (e.g. ¡Nuestras mejores prendas!)",
        ),
        slideInfo: str = Form(
            ...,
            description="""Slide information for the product slide:\n
Attributes:\n
title (str): Title of the slide,\n
desc (str): Description of the slide,\n
specifications (List[title (str): Title of the specification, desc (str): Description of the specification]): List of specifications for the slide.\n
    (e.g. {
        "slide_title":"Comodidad, durabilidad y estilo",
        "slide_desc":"¡Personaliza tus camisetas con nuestra innovadora tecnología!",
        "specifications":[
            {
                "specification_title":"Comodidad",
                "specification_desc":"Sin costuras y mayor suavidad de la tela."
            },
            {
                "specification_title":"Estilo",
                "specification_desc":"Diseños modernos y atractivos."
            }
        ]
    })""",
        ),
        file: UploadFile = File(..., description="Banner image for the product slide"),
    ) -> JSONResponse:
        try:
            slideInfoDict: Dict = json.loads(slideInfo)
            product_slide = ProductSlideSchema(
                title=title,
                desc=desc,
                banner="",
                slideInfo=slideInfoDict,
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=[
                    {"field": err.get("loc")[1], "msg": err.get("msg")}
                    for err in e.errors()
                ],
            )
        except Exception as e:
            error = e.__class__.__name__
            if error == "JSONDecodeError":
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=[
                        {
                            "field": "slideInfo",
                            "msg": "La información del slide no es válida",
                        }
                    ],
                )
        else:
            hash = await FileRequest().upload_slide_async(file=file)
            product_slide.banner = f"/read_slide?hash={hash.get('upload_dir')}"
            await ProductSlideModel.get_or_create_async(product_slide=product_slide)
            return JSONResponse(
                status_code=HTTP_201_CREATED,
                content={"slide": "OK"},
            )
