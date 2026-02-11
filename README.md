
---
**💁‍♀️ 🔗 Handy navigation links 🔗 💁‍♀️**

You are in the Application Setup Guide ---------------------------- 🗺️ `/my_little_bookworm`

- Jump to [Testing Guide](my_little_bookworm/tests/README.md) ------------- ⬅️ `/my_little_bookworm/tests` 
---

# Welcome to My Little Bookworm!

## About

My Little Bookworm is a web application which helps parents to keep track of how many books their pre-schooler children have read. The target is to read 1000 books before children start school, to support language development and educational outcomes. The app is written in React & Python + FastAPI with a SQL database. 

The app is a portfolio project by C27 students at Holberton School Australia. 

### Contributors
- Anna H
- Mel H
- Andrea M
- Maddy F
- Kat B


### Requirements

To get started, set up your virtual environment and install the project dependencies:
```
cd holbertonschool-portforlio_project
python3 -m venv venv
source venv/bin/activate   # Mac/Linux/WSL
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### Start the FastAPI Server

```
uvicorn app.main:app --reload
```

The `/user` endpoint can be tested with curl

```
# Post create_user(name, email)
curl -i -X POST 'http://127.0.0.1:8000/users' -H "Content-Type: application/json" -d '{"name": "Mary", "email": "mary@example.com"}'

# Return {user_info}
{"id":"1862d532-243e-413a-8c27-df61d23c5759","name":"Mary","email":"mary@example.com","role":"standard"}
```