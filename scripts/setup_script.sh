#!/usr/bin/bash
DB_HOST=host.docker.internal

# For Mel:
# DB_HOST=127.0.0.1

# Drop tables if exist
echo "Dropping tables..." 
mysql -h $DB_HOST -P 3306 -u root -p my_little_bookworm < app/persistence/seeds/reseed_helper.sql
echo "No more tables"

# Create tables
echo "Creating tables..."
PYTHONPATH=. python scripts/create_tables.py
echo "Tables recreated successfully!"

# Populate tables with seed data
echo "Seeding dev data..."
mysql -h $DB_HOST -P 3306 -u root -p my_little_bookworm < app/persistence/seeds/master_seed.sql
echo "🎉 Finished seeding data into my_little_bookworm 🎉"