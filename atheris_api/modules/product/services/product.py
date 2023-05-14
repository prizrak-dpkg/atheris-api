# Starlette imports
from typing import List
from beanie import PydanticObjectId
from starlette.status import HTTP_200_OK

# FastAPI imports
from fastapi.responses import JSONResponse

from atheris_api.modules.home.models.rating import RatingModel

# Own imports
from ..models.product import CustomerModel, ProductModel
from ..schemas.product import CustomerSchema, ProductSchema


class ProductRequest:
    async def create_async(
        self, customer: CustomerSchema, productList: List[ProductSchema]
    ) -> JSONResponse:
        _customer = await CustomerModel.create_async(customer=customer)
        for product in productList:
            await ProductModel.create_async(product=product, customer=_customer)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"hash": f"{_customer.id}"},
        )

    async def get_track_async(self, track: PydanticObjectId) -> JSONResponse:
        _customer = await CustomerModel.get(document_id=track)
        total = 0
        ready = 0
        status = 0
        rating = False
        if _customer:
            productList = await ProductModel.find(
                {"customer.$id": _customer.id}
            ).to_list()
            if await RatingModel.find({"owner": _customer.id}).first_or_none():
                rating = True
            for product in productList:
                total += 1
                if product.status:
                    ready += 1
        if total > 0:
            if _customer.status:
                status = 3
            elif ready == total:
                status = 2
            else:
                status = 1
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                "total": total,
                "ready": ready,
                "status": status,
                "rating": rating,
            },
        )
