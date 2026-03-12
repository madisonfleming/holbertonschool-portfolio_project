# scripts/create_tables.py

from app.persistence.sqlalchemy.db import engine
from app.persistence.sqlalchemy.tables import metadata

def main():
    print("Creating tables...")
    metadata.create_all(engine)
    print("Done.")

if __name__ == "__main__":
    main()
