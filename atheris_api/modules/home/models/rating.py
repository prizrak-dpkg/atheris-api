# Pydantic imports
import re
from typing import Optional
from pydantic import Field

# Beanie imports
from beanie import Document, Indexed, PydanticObjectId

# Own imports
from ..schemas.rating import RatingSchema


class RatingModel(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    comment: str = Field(...)
    qualification: float = Field(...)
    owner: Optional[PydanticObjectId] = Field(default=None)

    class Config:
        name = "ratings"

    @classmethod
    async def create_async(cls, rating: RatingSchema) -> "RatingModel":
        ratingQ = await cls.insert_one(
            cls(
                comment=rating.comment,
                qualification=rating.qualification,
                owner=rating.owner,
            )
        )
        if not isinstance(ratingQ, cls):
            raise Exception(
                "An unexpected error occurred when trying to get or create the "
                f"{cls.__name__} type object."
            )
        return ratingQ


models = [
    RatingModel,
]
