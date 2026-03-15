from sqlalchemy import create_engine
from app.config import get_settings
from dotenv import load_dotenv

# loads .env file to load the MYSQL_URL 
load_dotenv()

settings = get_settings()

MYSQL_URL = settings.DATABASE_URL  # Allow for dev, test & prod modes

if not MYSQL_URL:
    raise RuntimeError("MYSQL_URL is not set in the environment")

engine = create_engine(
    MYSQL_URL,
    echo=True,
    future=True,
)
