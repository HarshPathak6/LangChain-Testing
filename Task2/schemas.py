from pydantic import BaseModel


class ResumeRequest(BaseModel):
    resume: str


class ResumeResponse(BaseModel):
    name: str
    skills: list[str]
    years_of_experience: int
    last_role: str