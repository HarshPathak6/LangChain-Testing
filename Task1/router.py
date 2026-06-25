from fastapi import APIRouter

from Task1.schemas import PromptRequest, PromptResponse
from Task1.chains import transform_chain

router = APIRouter()


@router.post(
    "/transform",
    response_model=PromptResponse
)
def transform(request: PromptRequest):

    result = transform_chain.invoke(
        {
            "action": request.action,
            "text": request.text,
            "instruction": request.instruction
        }
    )

    return PromptResponse(
        response=result.content
    )