from typing import List

from fastapi import Query, APIRouter, HTTPException

from dto.filter_request import FilterRequest
from dto.page_response import PageResponse
from exceptions.page_exception import PageException
from orjson_response import ORJSONResponse
from service.dataset_service import filter_samples

samples_router = APIRouter(prefix="/veritas/api/samples", default_response_class=ORJSONResponse)


@samples_router.get("/{sample_id}", response_model=PageResponse)
async def get_sample_by_id(sample_id: int):
    return get_sample_by_id(sample_id)


@samples_router.get("/", response_model=PageResponse)
async def get_samples_by_filters(
        start_date: str = Query(
            None,
            title="Start Date",
            description="Filter by start date",
            example="2021-01-01T00:00:00.000Z",
        ),
        end_date: str = Query(
            None,
            title="End Date",
            description="Filter by end date",
            example="2021-01-01T00:00:00.000Z",
        ),
        max_likes: int = Query(
            None,
            title="Maximum Likes",
            description="Filter by maximum number of likes",
            ge=0,
            example=100,
        ),
        max_followers: int = Query(
            None,
            title="Maximum Followers",
            description="Filter by maximum number of followers",
            ge=0,
            example=1000,
        ),
        max_retweets: int = Query(
            None,
            title="Maximum Retweets",
            description="Filter by maximum number of retweets",
            ge=0,
            example=100,
        ),
        page: int = Query(
            0,
            title="Page Number",
            description="Page number for paginated results",
            ge=0,
            example=1,
        ),
        items_per_page: int = Query(
            5,
            title="Items Per Page",
            description="Number of items to return per page",
            ge=1,
            le=100,
            example=10,
        ),
):
    """
    Retrieve samples based on specific filters

    :raises HTTPException 400: Bad exception. Error occurred and handled on the backend.

    :raises HTTPException 500: Internal Server Error: Unhandled and unknown error on the backend.
    """
    try:
        filters = FilterRequest()
        filters.start_date = start_date
        filters.end_date = end_date
        filters.max_likes = max_likes,
        filters.max_followers = max_followers
        filters.max_retweets = max_retweets

        return filter_samples(filters, page, items_per_page)
    except PageException as ex:
        raise HTTPException(status_code=400, detail=ex.message)
