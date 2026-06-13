from app.models.base import Base
from sqlalchemy.orm import Mapped


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]