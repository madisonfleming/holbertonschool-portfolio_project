-- cleanup script to clear ALL DATA IN YOUR MySQL DATABASE
-- Navigate to persistence/seeds/ and run:
-- mysql -h 127.0.0.1 -P 3306 -u root -p my_little_bookworm < cleanup_script.sql
DELETE FROM MilestoneCompletion;
DELETE FROM MilestoneType;
DELETE FROM ReadingSession;
DELETE FROM Relationship;
DELETE FROM Child;
DELETE FROM Book;
DELETE FROM User;

SELECT 'All tables emptaaaaaay!' AS status;