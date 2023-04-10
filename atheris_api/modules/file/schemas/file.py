from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        default=None,
        alias="id",
        description="Unique identifier for the file",
    )
    sha256: str = Field(..., description="The sha256 hash of the file.")
    md5: str = Field(..., description="The md5 hash of the file.")
    ext: str = Field(..., description="File extension.")
