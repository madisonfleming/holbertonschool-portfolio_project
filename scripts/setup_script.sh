#!/usr/bin/bash

# DB_HOST is normally defined in .env. Set a default if unavailable:
if [[ -z "${DB_HOST}" ]]; then
    DB_HOST="127.0.0.1"
fi

# Drop tables if exist
echo "Dropping tables..." 
MYSQL_PWD="${DB_PASSWORD}" mysql -h $DB_HOST -P 3306 -u root my_little_bookworm < app/persistence/seeds/reseed_helper.sql
echo "No more tables"

# Create tables
echo "Creating tables..."
PYTHONPATH=. python3 scripts/create_tables.py
echo "Tables recreated successfully!"

# Populate tables with seed data
echo "Seeding dev data..."
MYSQL_PWD="${DB_PASSWORD}" mysql -h $DB_HOST -P 3306 -u root my_little_bookworm < app/persistence/seeds/master_seed.sql
echo "🎉 Finished seeding data into my_little_bookworm 🎉"