from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[CategoryORM]:
        result = await self.db.scalars(select(CategoryORM))
        return result.all()
    
    async def get_by_id(self, category_id: str) -> CategoryORM | None:
        return await self.db.get(CategoryORM, category_id)
    
    async def create_cat(self, name: str) -> CategoryORM:
        new_cat = CategoryORM(name=name)
        self.db.add(new_cat)
        return new_cat
    
    async def delete_cat(self, cat_for_del: CategoryORM) -> None:
        await self.db.delete(cat_for_del)
