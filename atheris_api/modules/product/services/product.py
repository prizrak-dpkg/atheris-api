# Starlette imports
from typing import List
from starlette.status import HTTP_200_OK

# FastAPI imports
from fastapi.responses import JSONResponse

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
