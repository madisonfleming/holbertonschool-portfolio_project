INSERT INTO MilestoneType (id, name, type, subject, threshold, created_at, updated_at)
VALUES
("4e977fea-a718-48ef-b85d-99feb16a1a6e", "Read 25 Books", "books_read", NULL, 25, NOW(), NOW()),
("a7652274-77e7-4d3a-be2b-e3822756b887", "Read 50 Books", "books_read", NULL, 50, NOW(), NOW()),
("dd41cd4f-1012-484d-b085-b5064b50bbd7", "Read 100 Books", "books_read", NULL, 100, NOW(), NOW()),
("c5fab157-0dd3-4079-8bee-38afa74049e2", "Read 150 Books", "books_read", NULL, 150, NOW(), NOW()),
("99e2e16b-0ce1-40b2-8f0d-2a7a15a69f55", "Read 200 Books", "books_read", NULL, 200, NOW(), NOW()),
("e8059b83-2cae-459d-876f-42027a200130", "Read 250 Books", "books_read", NULL, 250, NOW(), NOW()),
("f29932a4-60e3-4c71-bbd8-b6a4f1a1d97b", "Read 300 Books", "books_read", NULL, 300, NOW(), NOW()),
("4dcb447b-644d-44d0-9475-b9ca944141b1", "Read 350 Books", "books_read", NULL, 350, NOW(), NOW()),
("9c635ea4-5031-454d-96da-dc0bdbacb4b6", "Read 400 Books", "books_read", NULL, 400, NOW(), NOW()),
("64dc86b6-db1f-499a-96ca-980d5c6c2ce4", "Read 450 Books", "books_read", NULL, 450, NOW(), NOW()),
("d704b96f-8fdc-40dc-81fb-0a401a38a506", "Read 500 Books", "books_read", NULL, 500, NOW(), NOW()),
("2153e283-ea40-4e9a-9bb3-d0a76481856f", "Read 550 Books", "books_read", NULL, 550, NOW(), NOW()),
("fe3d1122-0855-4cec-a3de-855cf6b788de", "Read 600 Books", "books_read", NULL, 600, NOW(), NOW()),
("0f952f8e-f876-4e6a-8699-4ff1755406b5", "Read 650 Books", "books_read", NULL, 650, NOW(), NOW()),
("0f6207b0-fc13-4d80-9a44-624d54463bd0", "Read 700 Books", "books_read", NULL, 700, NOW(), NOW()),
("c5ecc441-0019-422b-90ee-8105379340e3", "Read 750 Books", "books_read", NULL, 750, NOW(), NOW()),
("8226c8ec-7968-4286-a71c-167083c73cce", "Read 800 Books", "books_read", NULL, 800, NOW(), NOW()),
("4a13cf87-3743-41c3-8f6b-7d5987cef449", "Read 850 Books", "books_read", NULL, 850, NOW(), NOW()),
("de0991b3-b5e9-4682-8a68-90ca4ba1b8bf", "Read 900 Books", "books_read", NULL, 900, NOW(), NOW()),
("624db84e-6bd6-4c04-9d69-6a2f6413e0ea", "Read 950 Books", "books_read", NULL, 950, NOW(), NOW()),
("2ce4f107-124e-45cf-9736-7f2f48db6379", "Read 1000 Books", "books_read", NULL, 1000, NOW(), NOW()),
("2d5b9437-2176-4c20-858c-c847b41beca3", "Read 5 Elephant Books", "weekly_goal", "elephants", 5, NOW(), NOW()),
("5efd791d-8034-4795-804a-fe735199fd18", "Read 5 Seahorse Books", "weekly_goal", "seahorses", 5, NOW(), NOW()),
("b3fbdc58-b059-432a-9092-56054a3e0254", "Read 5 Space Books", "weekly_goal", "space", 5, NOW(), NOW()),
("b2653090-ba4a-4c3a-9e49-5f2f1f86cce6", "Read 5 Dinosaur Books", "weekly_goal", "dinosaur", 5, NOW(), NOW());

SELECT 'MilestoneType seed was an overwhelming success' AS status;