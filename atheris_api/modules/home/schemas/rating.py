# Python imports
from typing import List, Optional

# Pydantic imports
from pydantic import BaseModel, Field, validator

# Beanie imports
from beanie import PydanticObjectId

# Own imports
from atheris_api.utils.paginate import PaginatedListSchema
from atheris_api.utils.regex import RegexEnum, RegexValidators


class RatingSchema(BaseModel):
    """
    Represents a rating schema.

    Attributes:
        id (Optional[PydanticObjectId]): Unique identifier for the rating.
        comment (str):Comment of the product.
        qualification (str): Qualification of the product.
    """

    id: Optional[PydanticObjectId] = Field(
        alias="_id",
        description="Unique identifier for the rating",
    )
    comment: str = Field(..., description="Comment of the product")
    qualification: float = Field(..., description="Qualification of the product")

    @validator("comment", pre=True, always=True)
    def check_title(cls, value: str) -> str:
        validator = (RegexValidators(regex=RegexEnum.TEXT, value=value)).validate
        if not validator.get("match"):
            raise ValueError(
                validator.get("message"),
            )
        return validator.get("value")

    @validator("qualification", pre=True, always=True)
    def check_desc(cls, value: float) -> float:
        if not value:
            raise ValueError("El campo * no puede estar vacío.")
        if value < 1.0:
            value = 1.0
        if value > 5.0:
            value = 5.0
        return value


class RatingSetSchema(RatingSchema):
    owner: PydanticObjectId = Field(..., description="Owner of the rating")


class RatingAverageSchema(RatingSchema):
    average: float = Field(..., description="Average of ratings")


class RatingListSchema(PaginatedListSchema):
    """
    Represents a response that contains a paginated list of RatingSchema objects.

    Attributes:
        results (List[RatingSchema]): List of products in the response.
    """

    results: List[RatingAverageSchema] = Field(
        ..., description="List of products in the response"
    )
