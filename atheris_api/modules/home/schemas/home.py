# Python imports
from typing import List, Optional

# Pydantic imports
from pydantic import BaseModel, Field, validator

# Beanie imports
from beanie import PydanticObjectId

# Own imports
from atheris_api.utils.paginate import PaginatedListSchema


class SpecificationSchema(BaseModel):
    """
    Represents a specification schema.

    Attributes:
        specification_title (str): Title of the specification.
        specification_desc (str): Description of the specification.
    """

    specification_title: str = Field(..., description="Title of the specification")
    specification_desc: str = Field(..., description="Description of the specification")

    @validator("specification_title", pre=True, always=True)
    def check_title(cls, value: str) -> str:
        if not value:
            raise ValueError("El campo * no puede estar vacío.")
        return value

    @validator("specification_desc", pre=True, always=True)
    def check_desc(cls, value: str) -> str:
        if not value:
            raise ValueError("El campo * no puede estar vacío.")
        return value


class SlideInfoSchema(BaseModel):
    """
    Represents a slide information schema.

    Attributes:
        slide_title (str): Title of the slide.
        slide_desc (str): Description of the slide.
        specifications (List[SpecificationSchema]): List of specifications for the slide.
    """

    slide_title: str = Field(..., description="Title of the slide")
    slide_desc: str = Field(..., description="Description of the slide")
    specifications: List[SpecificationSchema] = Field(
        ..., description="List of specifications for the slide"
    )

    @validator("slide_title", pre=True, always=True)
    def check_title(cls, value: str) -> str:
        if not value:
            raise ValueError("El campo * no puede estar vacío.")
        return value

    @validator("slide_desc", pre=True, always=True)
    def check_desc(cls, value: str) -> str:
        if not value:
            raise ValueError("El campo * no puede estar vacío.")
        return value


class ProductSlideSchema(BaseModel):
    """
    Represents a product slide schema.

    Attributes:
        id (Optional[PydanticObjectId]): Unique identifier for the product slide.
        title (str): Title of the product slide.
        desc (str): Description of the product slide.
        banner (str): URL of the banner image for the product slide.
        slideInfo (SlideInfoSchema): Slide information for the product slide.
    """

    id: Optional[PydanticObjectId] = Field(
        alias="_id",
        description="Unique identifier for the product slide",
    )
    title: str = Field(..., description="Title of the product slide")
    desc: str = Field(..., description="Description of the product slide")
    banner: str = Field(
        ..., description="URL of the banner image for the product slide"
    )
    slideInfo: SlideInfoSchema = Field(
        ..., description="Slide information for the product slide"
    )

    @validator("title", pre=True, always=True)
    def check_title(cls, value: str) -> str:
        if not value:
            raise ValueError("El campo * no puede estar vacío.")
        return value

    @validator("desc", pre=True, always=True)
    def check_desc(cls, value: str) -> str:
        if not value:
            raise ValueError("El campo * no puede estar vacío.")
        return value


class ProductSlideListSchema(PaginatedListSchema):
    """
    Represents a response that contains a paginated list of ProductSlideSchema objects.

    Attributes:
        results (List[ProductSlideSchema]): List of products in the response.
    """

    results: List[ProductSlideSchema] = Field(
        ..., description="List of products in the response"
    )
