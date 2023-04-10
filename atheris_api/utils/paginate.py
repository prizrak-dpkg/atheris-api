# Python imports
import math
import re
from typing import List, Tuple, TypeVar, Awaitable

# Pydantic imports
from pydantic import BaseModel

# Beanie imports
from beanie import Document


T = TypeVar("T", bound=Document)


class PaginatedListSchema(BaseModel):
    """
    Represents a response that contains information about the total number of
    records found, the number of possible pages, the current page number and
    the limit per page.
    """

    total: int
    num_pages: int
    current_page: int
    per_page: int


class PaginatedRequest:
    """
    A utility class for handling pagination in database queries.
    """

    async def get_query_by_field_async(
        self,
        cls: T,
        field: str,
        search: str,
        limit: int,
        page: int,
    ) -> Awaitable[Tuple[PaginatedListSchema, List[T]]]:
        """
        Returns a tuple of PaginatedListSchema and a list of objects of type T.

        :param cls: the class or subclass of Document to search.
        :param field: the field to search for.
        :param search: the search term to use.
        :param limit: the maximum number of documents to return.
        :param page: the page number (optional). If specified, it will calculate the new skip value.
        :return: a tuple containing a PaginatedListSchema and a list of objects of type T.
        """
        if limit < 1:
            limit = 1
        if limit > 100:
            limit = 100
        skip = (page - 1) * limit
        query = (
            {}
            if len(search.strip()) < 3
            else {f"{field}": {"$regex": f"{re.escape(search)}", "$options": "i"}}
        )
        results = await cls.find(query).skip(skip).limit(limit).to_list()
        total = await cls.find(query).count()
        return self._get_paginated_response(total, skip, limit, results)

    def _get_paginated_response(
        self, total: int, skip: int, limit: int, results: List[T]
    ) -> Tuple[PaginatedListSchema, List[T]]:
        """
        Returns a tuple of PaginatedListSchema and a list of objects of type T.

        :param total: the total number of documents.
        :param skip: the number of documents to skip.
        :param limit: the maximum number of documents to return.
        :param results: a list of objects of type T.
        :return: a tuple containing a PaginatedListSchema and a list of objects of type T.
        """
        num_pages = math.ceil(total / limit)
        current_page = int(skip / limit) + 1
        return (
            PaginatedListSchema(
                total=total,
                num_pages=num_pages,
                current_page=current_page,
                per_page=limit,
            ),
            results,
        )
