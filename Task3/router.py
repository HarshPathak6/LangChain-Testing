from fastapi import APIRouter

from Task3.schemas import QueryRequest, QueryResponse
from Task3.chains import ask

router = APIRouter()

@router.post(
    "/ask",
    response_model=QueryResponse
)
def ask_question(request: QueryRequest):

    result = ask(request.question)

    return QueryResponse(
        category=result["category"],
        answer=result["answer"]
    )