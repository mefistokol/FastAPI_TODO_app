from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class TaskORM(Base):
    __tablename__ = "tasks"
    
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)