from fastapi import Depends
from app.db.session import get_db
from app.services.task import TaskService
from app.services.category import CategoryService
from sqlalchemy.orm import Session



def get_cat_service(db: Session = Depends(get_db)):
    return CategoryService(db)

def get_task_service(db: Session = Depends(get_db)):
    return TaskService(db)
