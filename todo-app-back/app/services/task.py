from app.cache.redis import get_redis_cache
from app.core.config import get_settings
from app.repositories.task import TaskRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema

settings = get_settings()


class TaskNotFound(Exception):
    pass

class TaskService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)
        self.cache = get_redis_cache()
        
    async def list_tasks(self) -> list[TaskSchema]:
        cached_tasks = await self.cache.get(settings.cached_task_key)
        if cached_tasks is not None:
            return [TaskSchema.model_validate(task) for task in cached_tasks]
        
        tasks_orm = await self.task_repository.get_all()

        task_read = [TaskSchema.model_validate(task) for task in tasks_orm]
        tasks_for_cache = [task.model_dump() for task in task_read]
        await self.cache.set(settings.cached_task_key, tasks_for_cache)
        
        return task_read
    
    async def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = await self.task_repository.create(title=task_create.title)
        await self.db.commit()
        await self.db.refresh(task_orm)
        await self.cache.delete(settings.cached_task_key)
        return TaskSchema.model_validate(task_orm)
    
    async def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:

        task_for_update = await self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f'Задача с id {task_id} не найдена')
        
        
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        await self.db.commit()
        await self.db.refresh(task_for_update)

        await self.cache.delete(settings.cached_task_key)

        return TaskSchema.model_validate(task_for_update)
    
    async def delete_task(self, task_id: str) -> None:

        task_for_delete = await self.task_repository.get_by_id(task_id=task_id)

        if not task_for_delete:
            raise TaskNotFound(f'Задача с id {task_id} не найдена')
        
        await self.task_repository.delete_task(task_for_delete)
        
        await self.db.commit()

        await self.cache.delete(settings.cached_task_key)
