import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# loads .env file to load the MYSQL_URL 
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")

if not MYSQL_URL:
    raise RuntimeError("MYSQL_URL is not set in the environment")

engine = create_engine(
    MYSQL_URL,
    echo=True,
    future=True,
)
