from pathlib import Path

from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough
)

from LLMs.base import llm


PROMPT_DIR = Path(__file__).resolve().parent.parent / "Prompts" / "Task-4"


def load_prompt(file_name: str):

    with open(PROMPT_DIR / file_name, "r", encoding="utf-8") as f:

        return f.read()
    
    
tweet_chain = RunnableLambda(
    lambda topic: llm.invoke(
        load_prompt("tweet.txt").replace(
            "{text}",
            topic
        )
    )
)

linkedin_chain = RunnableLambda(
    lambda topic: llm.invoke(
        load_prompt("linkedin.txt").replace(
            "{text}",
            topic
        )
    )
)

hashtags_chain = RunnableLambda(
    lambda topic: llm.invoke(
        load_prompt("hashtags.txt").replace(
            "{text}",
            topic
        )
    )
)
    


parallel_chain = RunnableParallel(

    tweet=tweet_chain,
    linkedin=linkedin_chain,
    hashtags=hashtags_chain
)
    

chain = RunnablePassthrough() | parallel_chain


def generate_post(topic: str):

    result = chain.invoke(topic)

    hashtags = [
        tag.strip()
        for tag in result["hashtags"].content.split(",")
    ]

    return {

        "tweet": result["tweet"].content,

        "linkedin_caption": result["linkedin"].content,

        "hashtags": hashtags

    }