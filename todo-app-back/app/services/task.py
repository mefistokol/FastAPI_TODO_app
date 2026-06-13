from app.cache.redis import get_redis_cache
from app.core.config import get_settings
from app.repositories.task import TaskRepository
from sqlalchemy.orm import Session
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema

settings = get_settings()


class TaskNotFound(Exception):
    pass

class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)
        self.cache = get_redis_cache()
        
    def list_tasks(self) -> list[TaskSchema]:
        cached_tasks = self.cache.get(settings.cached_task_key)
        if cached_tasks is not None:
            return [TaskSchema.model_validate(task) for task in cached_tasks]
        
        tasks_orm = self.task_repository.get_all()

        task_read = [TaskSchema.model_validate(task) for task in tasks_orm]
        tasks_for_cache = [task.model_dump() for task in task_read]
        self.cache.set(settings.cached_task_key, tasks_for_cache)
        
        return task_read
    
    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:

        self.cache.delete(settings.cached_task_key)

        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        self.db.refresh(task_orm)
        return TaskSchema.model_validate(task_orm)
    
    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:

        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f'Задача с id {task_id} не найдена')
        
        
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        self.db.refresh(task_for_update)

        self.cache.delete(settings.cached_task_key)

        return TaskSchema.model_validate(task_for_update)
    
    def delete_task(self, task_id: str) -> None:

        task_for_delete = self.task_repository.get_by_id(task_id=task_id)

        if not task_for_delete:
            raise TaskNotFound(f'Задача с id {task_id} не найдена')
        
        self.task_repository.delete_task(task_for_delete)
        
        self.db.commit()

        self.cache.delete(settings.cached_task_key)