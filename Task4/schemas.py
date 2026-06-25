from pydantic import BaseModel

class ContentRequest(BaseModel):
    topic: str


class ContentResponse(BaseModel):
    tweet: str
    linkedin_caption: str
    hashtags: list[str]