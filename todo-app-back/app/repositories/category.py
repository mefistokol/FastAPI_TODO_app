from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()
    
    def get_by_id(self, category_id: str) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)
    
    def create_cat(self, name: str) -> CategoryORM:
        new_cat = CategoryORM(name=name)
        self.db.add(new_cat)
        return new_cat
    
    def delete_cat(self, cat_for_del: CategoryORM) -> None:
        self.db.delete(cat_for_del)