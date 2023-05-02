# Python imports
from datetime import datetime
from typing import Optional

# Pydantic imports
from pydantic import BaseModel, EmailStr, Field, validator

# Beanie imports
from beanie import PydanticObjectId

# Own imports
from atheris_api.utils.regex import RegexEnum, RegexValidators


class CustomerSchema(BaseModel):
    """
    Represents a product slide schema.

    Attributes:
        id (Optional[PydanticObjectId]): Unique identifier for the product slide.
        createdAt (datetime): Date and time the customer was created.
        documentNumber (str): Customer's document number.
        names (str): Customer's names.
        cellPhoneNumber (str): Customer's phone number.
        email (str): Customer's email address.
        city (str): Customer's city.
        address (str): Customer's address.
    """

    id: Optional[PydanticObjectId] = Field(
        alias="id",
        description="Unique identifier for the cutomer",
    )
    createdAt: datetime = Field(
        default_factory=datetime.utcnow,
        description="Date and time the customer was created",
    )
    documentNumber: str = Field(
        ...,
        description="Customer's document number",
    )
    names: str = Field(..., description="Customer's names")
    cellPhoneNumber: str = Field(
        ...,
        description="Customer's phone number",
    )
    email: EmailStr = Field(..., description="Customer's email address")
    city: str = Field(
        ...,
        description="Customer's city",
    )
    address: str = Field(
        ...,
        description="Customer's address",
    )

    @validator("documentNumber")
    def check_document_number(cls, document_number: str) -> str:
        validator = (
            RegexValidators(regex=RegexEnum.DOCUMENT_NUMBER, value=document_number)
        ).validate
        if not validator.get("match"):
            raise ValueError(
                validator.get("message"),
            )
        return validator.get("value")

    @validator("names")
    def check_names(cls, names: str) -> str:
        validator = (RegexValidators(regex=RegexEnum.WORD, value=names)).validate
        if not validator.get("match"):
            raise ValueError(
                validator.get("message"),
            )
        return validator.get("value")

    @validator("cellPhoneNumber")
    def check_cell_phone_number(cls, cell_phone_number: str) -> str:
        validator = (
            RegexValidators(regex=RegexEnum.CELL_PHONE_NUMBER, value=cell_phone_number)
        ).validate
        if not validator.get("match"):
            raise ValueError(
                validator.get("message"),
            )
        return validator.get("value")

    @validator("email", pre=True, always=True)
    def check_email(cls, email: str) -> str:
        validator = (RegexValidators(regex=RegexEnum.EMAIL, value=email)).validate
        if not validator.get("match"):
            raise ValueError(
                validator.get("message"),
            )
        return "{}".format(validator.get("value")).lower()

    @validator("city")
    def check_city(cls, city: str) -> str:
        validator = (RegexValidators(regex=RegexEnum.WORD, value=city)).validate
        if not validator.get("match"):
            raise ValueError(
                validator.get("message"),
            )
        return validator.get("value")

    @validator("address")
    def check_address(cls, address: str) -> str:
        validator = (RegexValidators(regex=RegexEnum.ADDRESS, value=address)).validate
        if not validator.get("match"):
            raise ValueError(
                validator.get("message"),
            )
        return validator.get("value")


class ProductColorsSchema(BaseModel):
    primaryColor: str = Field(..., description="Product's primary color")
    secondColor: str = Field(..., description="Product's second color")


class ProductSchema(BaseModel):
    """
    Represents a product slide schema.

    Attributes:
        id (Optional[PydanticObjectId]): Unique identifier for the product.
        createdAt (datetime): Date and time the product was created.
        primaryColor (str): Product's primary color.
        secondColor (str): Product's second color.
        chestWidth (int): Product's chest width.
        waistWidth (int): Product's waist width.
        neckToHipHeight (int): Product's neck to hip height.
        sleeveLengthShirt (int): Product's sleeve length t-shirt.
        sleeveLengthHoodie (int): Product's sleeve length hoodie.
        age (int): Product's age.
        height (int): Product's height.
        weight (int): Product's weight.
        shoeSize (int): Product's shoe size.
        bodyType (int): Product's body type.
        status (bool): Product's completion status.
    """

    id: Optional[PydanticObjectId] = Field(
        alias="id",
        description="Unique identifier for the product",
    )
    createdAt: datetime = Field(
        default_factory=datetime.utcnow,
        description="Date and time the product was created",
    )
    primaryColor: str = Field(..., description="Product's primary color")
    secondColor: str = Field(..., description="Product's second color")
    chestWidth: int = Field(..., description="Product's chest width")
    waistWidth: int = Field(..., description="Product's waist width")
    neckToHipHeight: int = Field(..., description="Product's neck to hip height")
    sleeveLengthShirt: int = Field(..., description="Product's sleeve length t-shirt")
    sleeveLengthHoodie: int = Field(..., description="Product's sleeve length hoodie")
    age: int = Field(..., description="Product's age")
    height: int = Field(..., description="Product's height")
    weight: int = Field(..., description="Product's weight")
    shoeSize: int = Field(..., description="Product's shoe size")
    bodyType: int = Field(..., description="Product's body type")
    status: bool = Field(default=False, description="Product's completion status")
