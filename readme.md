# Task API

A simple CRUD REST API built with **FastAPI** that demonstrates the basic CRUD (Create, Read, Update, Delete) operations on tasks.

---

## Features

- Create tasks
- Read all tasks
- Read a task by ID
- Update tasks
- Delete tasks
- Interactive Swagger documentation

---

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the project

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open Swagger UI in your browser:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |

---

## Example `curl -i`

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example output:

```text
HTTP/1.1 200 OK
content-type: application/json

[
  {
    "id": 1,
    "title": "Study FastAPI",
    "done": false
  },
  {
    "id": 2,
    "title": "Read book",
    "done": true
  },
  {
    "id": 3,
    "title": "Go to gym",
    "done": false
  }
]
```

---

## Swagger UI

![Swagger UI](images/Screenshot_22-7-2026_221724_127.0.0.1.jpeg)