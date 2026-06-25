from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_POOLSIDE_MODEL: str
    OPENROUTER_GEMMA_MODEL: str
    HUGGINGFACEHUB_ACCESS_TOKEN: str
    HUGGINGFACE_FASTCONTEXT_MODEL: str
    EMBEDDING_MODEL: str
    TEMPERATURE: float = 0.8
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()