from pydantic import BaseModel


class Task(BaseModel):
    title: str


class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None
