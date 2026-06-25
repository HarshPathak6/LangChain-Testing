from pydantic import BaseModel


class PromptRequest(BaseModel):
    action: str
    text: str
    instruction: str

class PromptResponse(BaseModel):
    response: str