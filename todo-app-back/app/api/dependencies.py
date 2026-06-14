from fastapi import Depends
from app.db.session import get_db
from app.services.task import TaskService
from app.services.category import CategoryService
from sqlalchemy.ext.asyncio import AsyncSession



async def get_cat_service(db: AsyncSession = Depends(get_db)):
    return CategoryService(db)

async def get_task_service(db: AsyncSession = Depends(get_db)):
    return TaskService(db)
