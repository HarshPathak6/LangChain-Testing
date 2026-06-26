from fastapi import APIRouter, HTTPException

from Task5.schemas import (
    SafeJsonRequest,
    SafeJsonResponse
)

from Task5.chains import generate_safe_json

router = APIRouter()


@router.post(
    "/safe-json",
    response_model=SafeJsonResponse
)
def safe_json(request: SafeJsonRequest):

    try:

        result = generate_safe_json(request.prompt)

        return SafeJsonResponse(
            data=result
        )

    except Exception:

        raise HTTPException(
            status_code=422,
            detail="Unable to generate valid JSON."
        )