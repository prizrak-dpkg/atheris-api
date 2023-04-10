# Pydantic imports
from pydantic import Field

# Beanie imports
from beanie import Document, Indexed, PydanticObjectId


class FileModel(Document):
    _id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="id")
    sha256: Indexed(str, unique=True) = Field(
        ..., description="The sha256 hash of the file."
    )
    md5: Indexed(str, unique=True) = Field(..., description="The md5 hash of the file.")
    ext: str = Field(..., description="File extension.")

    class Settings:
        name = "files"


models = [
    FileModel,
]
