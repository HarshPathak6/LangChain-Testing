from langchain_openai import ChatOpenAI
from config import settings
from LLMs.base import llm
from langchain_core.runnables import RunnableLambda, RunnableBranch


# Helper Function

def load_prompt(file_name: str, text: str, instruction: str):

    with open(file_name, "r", encoding="utf-8") as file:
        prompt = file.read()

    prompt = (
        prompt.replace("{text}", text),
        prompt.replace("{instruction}", instruction)
    )

    return prompt


# Individual Chains


def summarize(data):

    prompt = load_prompt(
        "Prompts/summary.txt",
        data["text"],
        data["instruction"]
    )

    return llm.invoke(prompt)


def translate(data):

    prompt = load_prompt(
        "Prompts/translate.txt",
        data["text"],
        data["instruction"]
    )

    return llm.invoke(prompt)


def tone_shift(data):

    prompt = load_prompt(
        "Prompts/tone.txt",
        data["text"],
        data["instruction"]
    )

    return llm.invoke(prompt)


# RunnableBranch

transform_chain = RunnableBranch(

    (
        lambda x: x["action"].lower() == "summarize",
        RunnableLambda(summarize)
    ),

    (
        lambda x: x["action"].lower() == "translate",
        RunnableLambda(translate)
    ),

    (
        lambda x: x["action"].lower() == "tone-shift",
        RunnableLambda(tone_shift)
    ),

    RunnableLambda(
        lambda _: llm.invoke(
            "Invalid action. Valid actions are summarize, translate and tone-shift."
        )
    )
)