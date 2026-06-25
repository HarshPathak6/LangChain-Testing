from langchain_openai import ChatOpenAI
from config import settings

llm = ChatOpenAI(
    model=settings.OPENROUTER_GEMMA_MODEL,
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=settings.TEMPERATURE,
)