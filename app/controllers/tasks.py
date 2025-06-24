from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.tasks import TaskCreate, TaskUpdate, TaskOut
from app.repository.tasks import create_task, mark_task_complete, get_user_tasks

router = APIRouter()

@router.post("/tasks/", response_model=TaskOut)
def create(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)

@router.put("/tasks/{task_id}/complete", response_model=TaskOut)
def complete(task_id: int, update: TaskUpdate, db: Session = Depends(get_db)):
    task = mark_task_complete(db, task_id, update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/tasks/user/{user_id}", response_model=list[TaskOut])
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    return get_user_tasks(db, user_id)
