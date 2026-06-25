from fastapi import APIRouter, UploadFile, File
from util.pdf import extract_text_from_pdf

from Task2.schemas import (
    ResumeRequest,
    ResumeResponse
)

from Task2.chains import parse_resume


router = APIRouter()


@router.post(
    "/parse-resume",
    response_model=ResumeResponse
)
def parse(request: ResumeRequest):

    result = parse_resume(request.resume)

    return result

@router.post(
    "/parse-resume-file",
    response_model=ResumeResponse
)
def parse_resume_file(
    resume: UploadFile = File(...)
):

    text = extract_text_from_pdf(resume.file)

    result = parse_resume(text)

    return result