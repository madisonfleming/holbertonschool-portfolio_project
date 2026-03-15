# Ensure test settings are applied first
import os
from app.config import get_settings

os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test.db"
settings = get_settings()
print(settings)
