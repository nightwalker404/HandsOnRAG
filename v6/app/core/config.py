from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    ### APP CONFIG ###
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8080)

    ### AI BASE VARS ###
    llm_model: str = Field(..., validation_alias="LLM_MODEL")
    ollama_url: str = Field(..., validation_alias="OLLAMA_URL")

    ### EMBEDDING MODEL ###
    embedding_model: str = Field(..., validation_alias="EMBEDDING_MODEL")

    ### CHROMA DB ###
    chroma_host: str = Field(..., validation_alias="CHROMA_HOST")
    chroma_port: int = Field(..., validation_alias="CHROMA_PORT")

@lru_cache
def get_settings():
    return Settings()
