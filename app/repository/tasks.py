from app.models.tasks import Task
from app.schema.tasks import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def mark_task_complete(db: Session, task_id: int, data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.is_completed = data.is_completed
        db.commit()
        db.refresh(task)
    return task

def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()
