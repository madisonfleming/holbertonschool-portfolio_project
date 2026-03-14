
-- Script to run all seeds at once. Used by scripts/setup_script.sh
-- To run this file directly from the seeds directory, either:
-- mysql -h 127.0.0.1 -P 3306 -u root -p my_little_bookworm < master_seed.sql
-- mysql -h host.docker.internal -P 3306 -u root -p my_little_bookworm < master_seed.sql

SOURCE app/persistence/seeds/seed_books.sql;
SOURCE app/persistence/seeds/seed_users.sql;
SOURCE app/persistence/seeds/seed_children.sql;
SOURCE app/persistence/seeds/seed_milestone_type.sql;
SOURCE app/persistence/seeds/seed_milestone_completion.sql;
SOURCE app/persistence/seeds/seed_reading_sessions.sql;
SOURCE app/persistence/seeds/seed_relationships.sql;

SELECT 'Master seed process completed, congrats :)' AS status;