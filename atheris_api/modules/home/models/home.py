# Pydantic imports
import re
from pydantic import Field

# Beanie imports
from beanie import Document, Indexed, PydanticObjectId

# Own imports
from ..schemas.home import ProductSlideSchema, SlideInfoSchema


class ProductSlideModel(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="id")
    title: Indexed(str, unique=True) = Field(...)
    desc: str = Field(...)
    banner: str = Field(...)
    slideInfo: SlideInfoSchema = Field(...)

    class Config:
        name = "productSlides"

    @classmethod
    async def get_or_create_async(
        cls, product_slide: ProductSlideSchema
    ) -> "ProductSlideModel":
        title_regex_pattern = f"^{re.escape(product_slide.title)}$"
        product_slideQ = await cls.find(
            {"title": {"$regex": title_regex_pattern, "$options": "i"}},
        ).first_or_none()
        if product_slideQ is None:
            product_slideQ = await cls.insert_one(
                cls(
                    title=product_slide.title,
                    desc=product_slide.desc,
                    banner=product_slide.banner,
                    slideInfo=product_slide.slideInfo,
                )
            )
        if not isinstance(product_slideQ, cls):
            raise Exception(
                "An unexpected error occurred when trying to get or create the "
                f"{cls.__name__} type object."
            )
        return product_slideQ


models = [
    ProductSlideModel,
]
