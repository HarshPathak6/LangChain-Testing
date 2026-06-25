from pathlib import Path

from langchain_core.runnables import RunnableLambda, RunnableBranch
from LLMs.base import llm


#PROMPT_DIR = Path("Prompts/Task-3")
PROMPT_DIR = Path(__file__).resolve().parent.parent / "Prompts" / "Task-3"


def load_prompt(file_name: str):
    with open(PROMPT_DIR / file_name, "r", encoding="utf-8") as f:
        return f.read()
    

def classify(question: str):

    prompt = f"""
You are a classifier.

Classify this question into ONLY one of these words.

coding
math
general

Question:
{question}

Answer with ONLY one word.
"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()

coding_chain = RunnableLambda(
    lambda x:
        llm.invoke(
            load_prompt("coding.txt").replace(
                "{text}",
                x["question"]
            )
        )
)

math_chain = RunnableLambda(
    lambda x:
        llm.invoke(
            load_prompt("math.txt").replace(
                "{text}",
                x["question"]
            )
        )
)

general_chain = RunnableLambda(
    lambda x:
        llm.invoke(
            load_prompt("general.txt").replace(
                "{text}",
                x["question"]
            )
        )
)

router = RunnableBranch(

    (
        lambda x: x["category"] == "coding",
        coding_chain
    ),

    (
        lambda x: x["category"] == "math",
        math_chain
    ),

    general_chain
)

def ask(question: str):

    category = classify(question)

    result = router.invoke(
        {
            "category": category,
            "question": question
        }
    )

    return {
        "category": category,
        "answer": result.content
    }