from app.cache.redis import get_redis_cache
from app.core.config import get_settings
from app.repositories.category import CategoryRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema

settings = get_settings()

class CategoryNotFound(Exception):
    pass

class CategoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.cat_repository = CategoryRepository(db)
        self.cache = get_redis_cache()
    
    async def list_categories(self) -> list[CategorySchema]:

        cached_cats = await self.cache.get(settings.cached_category_key)

        if cached_cats is not None:
            return [CategorySchema.model_validate(cat) for cat in cached_cats]
        
        cats_orm = await self.cat_repository.get_all()

        cats_read = [CategorySchema.model_validate(cat) for cat in cats_orm]
        cats_for_cache = [cat.model_dump() for cat in cats_read]
        await self.cache.set(settings.cached_category_key, cats_for_cache)

        return cats_read
    
    async def create_category(self, create_cat: CategoryCreateSchema) -> CategorySchema:
        cat_orm = await self.cat_repository.create_cat(name=create_cat.name)
        await self.db.commit()
        await self.db.refresh(cat_orm)
        await self.cache.delete(settings.cached_category_key)
        return CategorySchema.model_validate(cat_orm)
    
    async def update_category(self, cat_id: str, catupdate_cat: CategoryUpdateSchema) -> CategorySchema:

        cat_for_update = await self.cat_repository.get_by_id(cat_id)

        if not cat_for_update:
            raise CategoryNotFound('Category not found')

        if catupdate_cat.name is not None:
            cat_for_update.name = catupdate_cat.name

        await self.db.commit()
        await self.db.refresh(cat_for_update)

        await self.cache.delete(settings.cached_category_key)

        return CategorySchema.model_validate(cat_for_update)
    
    async def delete_category(self, cat_id: str) -> None:

        cat_for_delete = await self.cat_repository.get_by_id(cat_id)

        if not cat_for_delete:
            raise CategoryNotFound('Category not found')
        
        await self.cat_repository.delete_cat(cat_for_delete)

        await self.db.commit()

        await self.cache.delete(settings.cached_category_key)
