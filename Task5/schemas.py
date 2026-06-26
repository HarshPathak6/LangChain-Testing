from typing import Any
from pydantic import BaseModel


class SafeJsonRequest(BaseModel):
    prompt: str


class SafeJsonResponse(BaseModel):
    data: dict[str, Any]