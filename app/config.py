from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "MyLittleBookworm"
    DEBUG: bool = False
    # Enable the next two lines to guarantee that prod
    # won't start without these values
    # DATABASE_URL: str
    # SECRET_KEY: str

class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True

class ProductionConfig(BaseConfig):
    DEBUG: bool = False

class TestingConfig(BaseConfig):
    DEBUG: bool = True
    # DATABASE = 'sqlite:///:memory:'
    # SECRET_KEY: str = "test-secret-key"

def get_settings_class():
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        return ProductionConfig
    
    if env == "testing":
        return TestingConfig
    
    return DevelopmentConfig