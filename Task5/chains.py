import json

from pathlib import Path

from langchain_core.runnables import RunnableLambda

from LLMs.base import llm



PROMPT_DIR = Path(__file__).resolve().parent.parent / "Prompts" / "Task-5"


def load_prompt(file_name: str):
    with open(PROMPT_DIR / file_name, "r", encoding="utf-8") as f:
        return f.read()


def first_attempt(text: str):

    prompt = load_prompt("safe_json.txt").replace("{text}", text)

    response = llm.invoke(prompt)

    return response.content


def repair_json(data):

    try:

        parsed = json.loads(data)

        return parsed

    except Exception as e:

        fix_prompt = f"""
Your previous response was NOT valid JSON.

Parser Error:

{e}

Previous Output:

{data}

Return ONLY corrected JSON.

Nothing else.
"""

        fixed = llm.invoke(fix_prompt)

        parsed = json.loads(fixed.content)

        return parsed


chain = RunnableLambda(first_attempt) | RunnableLambda(repair_json)


def generate_safe_json(prompt: str):

    return chain.invoke(prompt)