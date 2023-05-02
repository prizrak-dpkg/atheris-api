# Pydantic imports
from datetime import datetime

# Pydantic imports
from pydantic import EmailStr, Field

# Beanie imports
from beanie import Document, Link, PydanticObjectId

# Own imports
from ..schemas.product import CustomerSchema, ProductSchema


class CustomerModel(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="created_at")
    document_number: str = Field(...)
    names: str = Field(...)
    cell_phone_number: str = Field(...)
    email: EmailStr = Field(...)
    city: str = Field(...)
    address: str = Field(...)

    class Config:
        name = "customers"

    @classmethod
    async def create_async(cls, customer: CustomerSchema) -> "CustomerModel":
        customerQ = await cls.insert_one(
            cls(
                created_at=customer.createdAt,
                document_number=customer.documentNumber,
                names=customer.names,
                cell_phone_number=customer.cellPhoneNumber,
                email=customer.email,
                city=customer.city,
                address=customer.address,
            )
        )
        if not isinstance(customerQ, cls):
            raise Exception(
                "An unexpected error occurred when trying to get or create the "
                f"{cls.__name__} type object."
            )
        return customerQ


class ProductModel(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="created_at")
    primary_color: str = Field(...)
    second_color: str = Field(...)
    chest_width: int = Field(...)
    waist_width: int = Field(...)
    neck_to_hip_height: int = Field(...)
    sleeve_length_shirt: int = Field(...)
    sleeve_length_hoodie: int = Field(...)
    age: int = Field(...)
    height: int = Field(...)
    weight: int = Field(...)
    shoe_size: int = Field(...)
    body_type: int = Field(...)
    status: bool = Field(...)
    customer: Link[CustomerModel]

    class Config:
        name = "products"

    @classmethod
    async def create_async(
        cls, product: ProductSchema, customer: CustomerModel
    ) -> "CustomerModel":
        customerQ = await cls.insert_one(
            cls(
                created_at=product.createdAt,
                primary_color=product.primaryColor,
                second_color=product.secondColor,
                chest_width=product.chestWidth,
                waist_width=product.waistWidth,
                neck_to_hip_height=product.neckToHipHeight,
                sleeve_length_shirt=product.sleeveLengthShirt,
                sleeve_length_hoodie=product.sleeveLengthHoodie,
                age=product.age,
                height=product.height,
                weight=product.weight,
                shoe_size=product.shoeSize,
                body_type=product.bodyType,
                status=product.status,
                customer=customer,
            )
        )
        if not isinstance(customerQ, cls):
            raise Exception(
                "An unexpected error occurred when trying to get or create the "
                f"{cls.__name__} type object."
            )
        return customerQ


models = [
    CustomerModel,
    ProductModel,
]
