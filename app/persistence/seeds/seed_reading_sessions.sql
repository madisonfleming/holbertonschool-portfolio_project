SET @book_count = (SELECT COUNT(*) FROM Book);

-- Create 999 reading sessions for Stella
INSERT INTO ReadingSession (id, child_id, external_id, book_id, title, cover_url, logged_at, created_at, updated_at)
WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM seq WHERE n < 999
),
numbered_books AS (
  SELECT ROW_NUMBER() OVER () AS rn, id, external_id, title, cover_url
  FROM Book
)
SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429111",
  b.external_id,
  b.id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN numbered_books b ON b.rn = (seq.n % @book_count) + 1

-- Create 199 reading sessions for Betty
UNION ALL

SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429222",
  b.external_id,
  b.id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN numbered_books b ON b.rn = ((seq.n - 1) % @book_count) + 1
WHERE seq.n <= 199

-- Create 80 reading sessions for Tommy
UNION ALL

SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429333",
  b.external_id,
  b.id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN numbered_books b ON b.rn = (
  (seq.n - 1) % @book_count) + 1
WHERE seq.n <= 80

-- Create 32 reading sessions for Billy
UNION ALL

SELECT
  UUID(),
  "e686c824-25e6-4704-87a6-651938429444",
  b.external_id,
  b.id,
  b.title,
  b.cover_url,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY,
  NOW() - INTERVAL FLOOR(RAND()*180) DAY
FROM seq
JOIN numbered_books b ON b.rn = ((seq.n - 1) % @book_count) + 1
WHERE seq.n <= 32;

SELECT 'Yeehaw we have SO MANY reading sessions!!!!' AS status;