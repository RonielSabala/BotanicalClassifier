"""
This module loads Azure Custom Vision API credentials from
environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

from .paths import DOTENV_PATH


class Settings(BaseSettings):
    custom_vision_key: str
    custom_vision_endpoint: str
    custom_vision_project_id: str
    custom_vision_published_name: str

    model_config = SettingsConfigDict(env_file=DOTENV_PATH)


# Global singleton
settings = Settings()  # pyright: ignore[reportCallIssue]
