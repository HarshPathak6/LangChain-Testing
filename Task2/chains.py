from LLMs.base import llm

from Task2.schemas import ResumeResponse


def parse_resume(text: str):

    with open(
        "Prompts/resume_parser.txt",
        "r",
        encoding="utf-8"
    ) as file:

        prompt = file.read()

    prompt = prompt.replace("{text}", text)

    structured_llm = llm.with_structured_output(
        ResumeResponse
    )

    return structured_llm.invoke(prompt)