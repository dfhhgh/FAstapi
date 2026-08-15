# Task API

A CRUD REST API built with **FastAPI**, **PostgreSQL**, and **Docker Compose** for task management.

---

## Features

- Create, read, update, and delete tasks
- Persistent data storage with PostgreSQL
- Containerized with Docker Compose
- Repository abstraction for swappable storage
- Interactive Swagger documentation

---

## Architecture

```text
HTTP Request
  ↓
Router
  ↓
TaskService
  ↓
TaskRepository
  ↓
PostgresTaskRepository
  ↓
PostgreSQL
```

The application uses a repository abstraction. `TaskRepository` defines the storage interface, and `PostgresTaskRepository` implements it with PostgreSQL.

The service and route layers remained unchanged when SQLiteTaskRepository was replaced by PostgresTaskRepository in A3.

---

## PostgreSQL

The application uses PostgreSQL as its persistent database.

| Property | Value |
|----------|-------|
| PostgreSQL version | 16 |
| Database | `tasksdb` |
| Compose service name | `db` |
| Persistent storage | Docker named volume `pgdata` |

PostgreSQL runs inside a Docker container. Data is persisted using the Docker named volume `pgdata`. Docker may display the actual volume name with the Compose project prefix, such as `fastapi_pgdata`.

---

## Environment Variables

The application uses the `DATABASE_URL` environment variable to connect to PostgreSQL.

| File | Committed | Description |
|------|-----------|-------------|
| `.env` | No (gitignored) | Local/private configuration |
| `.env.example` | Yes | Template for `.env` |

Inside Docker Compose, PostgreSQL is reached using the Compose service name `db`:

```text
postgresql://user:password@db:5432/tasksdb
```

---

## Run with Docker Compose

The primary way to start the project is with Docker Compose:

```bash
docker compose up --build
```

This starts both services:

- **FastAPI** application
- **PostgreSQL** database

The application is available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

The PostgreSQL database and `tasks` table are created automatically on first startup. No manual database setup is required.

### Safe restart

```bash
docker compose down
docker compose up -d
```

By default, `docker compose down` removes the containers and networks but preserves named volumes, so PostgreSQL data remains available when the stack is started again.

**Do not use** `docker compose down -v` because `-v` removes the volume and destroys all persisted data.

### Docker architecture

```text
FastAPI container
    |
    | db:5432
    ↓
PostgreSQL container
    |
    ↓
Docker named volume: pgdata
```

---

## SQL Initialization

The file `sql/init.sql` creates the `tasks` table:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
```

PostgreSQL initialization scripts in `/docker-entrypoint-initdb.d/` run during first-time database initialization only. They do not run every time `docker compose up` is executed against an already initialized volume.

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
curl -i http://localhost:8000/tasks
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

## Persistence Verification

Persistence was verified by testing that task data survives both application and PostgreSQL container restarts without removing the Docker volume.

### Test performed

1. Two tasks were created through `POST /tasks`.
2. The rows were confirmed directly in PostgreSQL.
3. The FastAPI container was restarted (`docker compose restart app`). The tasks remained available.
4. The PostgreSQL container was restarted (`docker compose restart db`). The tasks remained available.
5. The PostgreSQL container was removed and recreated (`docker compose stop db`, `docker compose rm -f db`, `docker compose up -d db`). The Docker PostgreSQL volume was **not** deleted.
6. The same tasks remained available after recreation.
7. PostgreSQL was queried directly again to confirm the rows still existed.

### Conclusion

This proves persistence through the Docker named volume `pgdata`. Stopping and recreating the PostgreSQL container reattaches the same volume, preserving all data.

---

## Swagger UI

![Swagger UI](images/Screenshot_22-7-2026_221724_127.0.0.1.jpeg)

---

## Optional Local Development (A2 historical)

The following commands are from the earlier A2 setup that used SQLite. They are not the primary way to run the current A3 project.

```bash
pip install -r requirment.txt
uvicorn Fast:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## A2 SQLite History

In A2, the application used **SQLite** as its storage backend.

A2 storage flow:

```text
SQLiteTaskRepository
  ↓
SQLite (tasks.db)
```

A3 storage flow:

```text
PostgresTaskRepository
  ↓
PostgreSQL (Docker)
```

### Why SQLite was used in A2

SQLite was chosen for A2 because:

- It is lightweight and requires no configuration.
- It does not require a separate database server to run.
- The entire database is stored in a single local file (`tasks.db`).
- It was well-suited for the learning project in A2.

### SQLite database viewer

The SQLite database was inspected using DB Browser for SQLite.

![SQLite Database Viewer](images/stage4-database.png)

### Example SQL query (A2)

The following query was executed during A2 Stage 4 using DB Browser for SQLite:

```sql
SELECT * FROM tasks WHERE done = 1;
```

This query returns only the completed tasks (where `done` is `1` / `true`).

### Stage 4 verification (A2)

During A2 Stage 4, the database was manually modified using DB Browser for SQLite.

For example, after running:

```sql
UPDATE tasks SET done = 1;
```

the `GET /tasks` endpoint confirmed that all tasks now had `done: true`. This verified that the API reads directly from the database.

---

## A3 Containerization Summary

A3 demonstrates the following:

- **PostgreSQL in Docker**: PostgreSQL 16 runs as a containerized service.
- **Persistent Docker volume**: The named volume `pgdata` ensures data survives container restarts and recreation.
- **Repository abstraction**: `TaskRepository` defines the storage interface.
- **PostgresTaskRepository**: Implements the repository interface with PostgreSQL using `psycopg`.
- **Docker Compose**: `docker compose up --build` starts the full stack (FastAPI + PostgreSQL).
- **Environment-based configuration**: `DATABASE_URL` is set via environment variables. Secrets are in `.env` (gitignored).
- **Persistence across container recreation**: Data survives PostgreSQL container removal and recreation as long as the volume is preserved.

The application storage was switched by replacing the repository implementation and updating the dependency wiring, while the service and route layers remained unchanged. Docker, SQL initialization, and environment configuration were added to containerize the stack.
