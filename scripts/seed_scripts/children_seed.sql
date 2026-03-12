INSERT INTO Child (id, name, date_of_birth, avatar_url, created_at, updated_at)
VALUES
("e686c824-25e6-4704-87a6-651938429111", "Stella", "2018-01-01", "/avatars/mlb-avatar-sun", NOW(), NOW()),
("e686c824-25e6-4704-87a6-651938429222", "Betty", "2017-05-12", "/avatars/mlb-avatar-bee", NOW(), NOW()),
("e686c824-25e6-4704-87a6-651938429333", "Tommy", "2016-09-03", "/avatars/mlb-avatar-robot", NOW(), NOW()),
("e686c824-25e6-4704-87a6-651938429444", "Billy", "2015-11-20", "/avatars/mlb-avatar-sun", NOW(), NOW());
SELECT 'Child seed was a massive success' AS status;