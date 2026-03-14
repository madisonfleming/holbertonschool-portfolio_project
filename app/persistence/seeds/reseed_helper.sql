-- cleanup script to drop all tables and data before re-seeding
DROP TABLE IF EXISTS
MilestoneType, MilestoneCompletion, ReadingSession, Relationship, Child, Book, User;

SELECT 'Dropped all tables' AS status;