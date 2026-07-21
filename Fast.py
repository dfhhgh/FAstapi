from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
app=FastAPI()

@app.get('/')
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

class Task(BaseModel):
    title:str
@app.get('/health')
async def health():
    return { "status": "ok" }

tasks = [
    {
        "id": 1,
        "title": "Study FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Read book",
        "done": True
    },
    {
        "id": 3,
        "title": "Go to gym",
        "done": False
    }
]
@app.get('/tasks')
async def gettasks():
    return tasks
@app.get('/tasks/{id}')
async def gettask(id:int):
    for task in tasks:
        if task['id']==id:
            return task
    raise HTTPException (status_code=404, detail=f"Task {id} not found" )

@app.post('/tasks',status_code=201)
async def posttask(task:Task):
    if not  task.title.strip():
        tasks.append(
        {
            "id":tasks[-1]["id"] + 1,
            "title": task.title,
            "done": False
        }
        )
        return tasks[-1]
    raise HTTPException (status_code=400, detail="Title cannot be empty"  )



    
