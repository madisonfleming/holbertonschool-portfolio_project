-- Recursively generates up to 999 rows to insert
WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM seq WHERE n < 999
)

-- Create 999 reading sessions for Stella
INSERT INTO ReadingSession (id, child_id, external_id, book_id, title, cover_url, logged_at, created_at, updated_at)
SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429111",
  b.external_id,
  b.book_id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN books b ON b.id = (
  SELECT id
  FROM books
  LIMIT 1 OFFSET (n % (SELECT COUNT(*) FROM books))
)

-- Create 199 reading sessions for Betty

UNION ALL

SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429222",
  b.external_id,
  b.book_id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN books b ON b.id = (
  SELECT id
  FROM books
  LIMIT 1 OFFSET ((n - 1) % (SELECT COUNT(*) FROM books))
)
WHERE n <= 199

-- Create 80 reading sessions for Tommy

UNION ALL

SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429333",
  b.external_id,
  b.book_id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN books b ON b.id = (
  SELECT id
  FROM books
  LIMIT 1 OFFSET ((n - 1) % (SELECT COUNT(*) FROM books))
)
WHERE n <= 80

-- Create 32 reading sessions for Billy
UNION ALL

SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429444",
  b.external_id,
  b.book_id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN books b ON b.id = (
  SELECT id
  FROM books
  LIMIT 1 OFFSET ((n - 1) % (SELECT COUNT(*) FROM books))
)
WHERE n <= 32;