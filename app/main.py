from fastapi import FastAPI

from app.postgres_repository import PostgresTaskRepository
from app.service import TaskService
from app.router import router
from app.auth_router import auth_router
from app.gates_router import gates_router
from app.supabase_client import SUPABASE_URL, SUPABASE_KEY

app = FastAPI()

repository = PostgresTaskRepository()
task_service = TaskService(repository)

app.include_router(auth_router)
app.include_router(gates_router)
app.include_router(router)


@app.on_event("startup")
def startup():
    if SUPABASE_URL and SUPABASE_KEY:
        print("Supabase configuration loaded successfully")
    else:
        print("WARNING: Supabase configuration not found")
