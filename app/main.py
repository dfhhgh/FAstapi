from fastapi import FastAPI

from app.postgres_repository import PostgresTaskRepository
from app.service import TaskService
from app.router import router

app = FastAPI()

repository = PostgresTaskRepository()
task_service = TaskService(repository)

app.include_router(router)
