from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application configuration loaded from environment variables.

    Values are read from process env and an optional .env file in the project root.
    """

    app_env: str = Field(default="local")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")

    llm_api_key: str = Field(default="")
    llm_model_name:str = Field(default="")


    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()