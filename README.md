
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


### Requirements

To get started, set up your virtual environment and install the project dependencies:
```
cd holbertonschool-portforlio_project
python3 -m venv venv
source venv/bin/activate   # Mac/Linux/WSL
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

**Upon running `pip install`, WSL users may encounter the following error, even from
within a virtual environment:**
`error: externally-managed-environment`
This happens because Python 3.12+ on Ubuntu/WSL enforces PEP 668 protections.
To bypass this *safely from inside your venv*, install dependencies using:
```
pip install --break-system-packages -r requirements.txt
```

### ⚡ Start the FastAPI Server ⚡

```
uvicorn app.main:app --reload
```

## Testing the API with cURL

The endpoints can be tested with curl:

### Users

**Create a user**
```
curl -i -X POST 'http://127.0.0.1:8000/users' \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mary",
    "email": "mary@example.com",
    "firebase_uid": "7UKtP5I8lBbDoO8wVv6WB8Ge03Q2"
  }'
```
Expected:

```
{
  "id":"ed99ba2d-66b4-4c35-b76f-ea40a96fb6be",
  "name": "Mary",
  "email": "mary@example.com",
  "role": "standard"
}
```

### Children

**Create a child**
```
curl -i -X POST 'http://127.0.0.1:8000/children' \
  -H "Content-Type: application/json" \
  -d '{"parent_id": "<user_id>", "name": "Sophie", "age": 5}'
```
<br>
<br>

## 🚀 Frontend (React + Vite) 🚀

The frontend is located in the `react-app` directory and uses **Vite** for fast development builds. 

### Install dependencies:

```
cd react-app
npm install
npm i react-router-dom
npm install react-bootstrap bootstrap
```

### Start the dev server
```
npm run dev             # for WSL
npm run dev -- --host   # containers, LAN, mobile testing
```

Vite will start the app and display a local development URL, usually:
`http://localhost:5173/`
