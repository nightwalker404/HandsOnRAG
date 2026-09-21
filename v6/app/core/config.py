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

    ### Qdrant ###
    qdrant_host: str = Field(..., validation_alias="QDRANT_HOST")
    qdrant_port: int = Field(..., validation_alias="QDRANT_PORT")
    qdrant_collection: str = Field(..., validation_alias="QDRANT_COLLECTION")

    ### S3 GARAGE OBJECT STORAGE ###
    garage_endpoint: str = Field(..., validation_alias="GARAGE_ENDPOINT")
    garage_region: str = Field(..., validation_alias="GARAGE_REGION")
    garage_access_key: str = Field(..., validation_alias="GARAGE_ACCESS_KEY")
    garage_secret_key: str = Field(..., validation_alias="GARAGE_SECRET_KEY")
    garage_bucket: str = Field(..., validation_alias="GARAGE_BUCKET")

@lru_cache
def get_settings():
    return Settings()
