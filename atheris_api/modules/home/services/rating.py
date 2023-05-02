# Starlette imports
from functools import reduce
from typing import List
from starlette.status import HTTP_201_CREATED

# FastAPI imports
from fastapi import Body
from fastapi.responses import JSONResponse

# Own imports
from atheris_api.modules.home.models.rating import RatingModel
from atheris_api.modules.home.schemas.rating import (
    RatingSchema,
    RatingAverageSchema,
    RatingListSchema,
)
from atheris_api.utils.paginate import PaginatedListSchema, PaginatedRequest


class RatingRequest(PaginatedRequest):
    async def get_async(
        self, limit: int = 1, page: int = 1, comment: str = ""
    ) -> RatingListSchema:
        results: List[RatingAverageSchema] = []
        ratings: List[RatingModel]
        page_information: PaginatedListSchema
        page_information, ratings = await self.get_query_by_field_async(
            RatingModel, "comment", comment, limit, page
        )
        all_ratings = await RatingModel.find_all().limit(1000).to_list()
        total_qualification = reduce(
            lambda acc, rating: acc + rating.qualification, all_ratings, 0
        )
        ratings_count = 1 if len(all_ratings) == 0 else len(all_ratings)
        average = total_qualification / ratings_count
        for rating in ratings:
            results.append(
                RatingAverageSchema(
                    id=rating.id,
                    comment=rating.comment,
                    qualification=rating.qualification,
                    average=average,
                )
            )
        return RatingListSchema(
            total=page_information.total,
            num_pages=page_information.num_pages,
            current_page=page_information.current_page,
            per_page=page_information.per_page,
            results=results,
        )

    async def create_rating_async(
        self,
        rating: RatingSchema = Body(...),
    ) -> JSONResponse:
        await RatingModel.create_async(rating=rating)
        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content={"rating": "OK"},
        )
