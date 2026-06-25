from fastapi import APIRouter

from Task4.schemas import (
    ContentRequest,
    ContentResponse
)

from Task4.chains import generate_post

router = APIRouter()


@router.post(
    "/generate-post",
    response_model=ContentResponse
)
def generate(request: ContentRequest):

    result = generate_post(request.topic)

    return ContentResponse(

        tweet=result["tweet"],

        linkedin_caption=result["linkedin_caption"],

        hashtags=result["hashtags"]

    )