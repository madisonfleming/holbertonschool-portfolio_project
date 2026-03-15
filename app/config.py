from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    ENVIRONMENT: str = "development"
    APP_NAME: str = "MyLittleBookworm"
    DEBUG: bool = False
    FIREBASE_CONFIG: str = "app/config/serviceAccountKey.json"
    DATABASE_URL: str

class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True

class ProductionConfig(BaseConfig):
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

class UnitTestingConfig(BaseConfig):
    model_config = SettingsConfigDict(extra="ignore")
    
    ENVIRONMENT: str = "testing"
    DEBUG: bool = True
    FIREBASE_CONFIG: str = ""
    DATABASE_URL: str = "sqlite+pysqlite:///./test.db"


def get_settings_class():
    base = BaseConfig()
    env = base.ENVIRONMENT.lower()

    if env == "production":
        return ProductionConfig
    
    if env == "testing":
        return UnitTestingConfig
    
    return DevelopmentConfig

@lru_cache
def get_settings():
    settings_class = get_settings_class()
    return settings_class()
