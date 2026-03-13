
-- Script to run all seeds at once.
-- Navigate to persistence/seeds/ and run:
-- mysql -h 127.0.0.1 -P 3306 -u root -p my_little_bookworm < master_seed.sql

SOURCE ./seed_books.sql;
SOURCE ./seed_children.sql;
SOURCE ./seed_milestone_type.sql;
SOURCE ./seed_milestone_completion.sql;
SOURCE ./seed_reading_sessions.sql;
SOURCE ./seed_relationships.sql;
SOURCE ./seed_users.sql;