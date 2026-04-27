
---
**💁‍♀️ 🔗 Handy navigation links 🔗 💁‍♀️**

You are in the Application Setup Guide ---------------------------- 🗺️ `/my_little_bookworm`

- Jump to [Testing Guide](/tests/README.md) ------------- ⬅️ `/my_little_bookworm/tests` 

---

# 📖 Welcome to My Little Bookworm! 🐛

## About

My Little Bookworm is a web application which helps parents to keep track of how many books their pre-schooler children have read. The target is to read 1000 books before children start school, to support language development and educational outcomes. The app is written in React & Python + FastAPI with a SQL database. 

The app is a portfolio project by C27 students at Holberton School Australia. 

### 👥 Contributors 👥
- Anna H
- Mel H
- Andrea M
- Maddy F
- Kat B

### Tech Stack

Front end: React & Vite
Backend: Python & FastAPI & SQLAlchemy
Database: MySQL

### Getting Started

    Note to project members: The old setup process relied on manually running the start commands for each service inside a single docker container, and the new setup separates out the front-end, back-end and database into separate containers and uses a single command to start all services. If you're converting your local env from the old setup process to the new one, you'll need to re-clone the repo and copy the required files across to the newly cloned repo before using docker compose. Once it's running, you can delete the old container and free up space on your hard drive.

1. Fork & clone the repo
2. Create a `.env` file in the project root, using the variables in `.env-example` as a template

- Copy MLB's Vite Firebase & DB config values across from our project documentation, or BYO Firebase values

3. Create a file in `app/config/serviceAccountKey.json`

- Copy Firebase auth config across from our project documentation, or BYO Firebase account details

4. Install docker tools if you don't already have them
5. Start the app locally with `docker compose`

```bash
# run from project root

docker compose up -d
```

Docker will start 3 containers:

- frontend (hosting a Vite Server)
- backend (hosting a FastAPI Server)
- mysql (hosting a MySQL v8 db)

6. One the db container is running, seed the database using the seed scripts

```bash
docker exec -it holbertonschool-portfolio_project-backend-1 bash -c "source scripts/setup_script.sh"
```

### Access the app

When the containers are ready, the application and the backend API docs can be accessed via:

- localhost:5173
- localhost:8000/docs

Sign in with any of the seeded users

- login details are available in the project documentation
- Patrick is configured to use log in via Google, everyone else uses username/password