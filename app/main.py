from fastapi import FastAPI

from app.database import init_db
from app.sqlite_repository import SQLiteTaskRepository
from app.service import TaskService
from app.router import router

app = FastAPI()

repository = SQLiteTaskRepository()
task_service = TaskService(repository)

app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()
