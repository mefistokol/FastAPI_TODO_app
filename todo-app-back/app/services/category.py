from app.cache.redis import get_redis_cache
from app.core.config import get_settings
from app.repositories.category import CategoryRepository
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema

settings = get_settings()

class CategoryNotFound(Exception):
    pass

class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.cat_repository = CategoryRepository(db)
        self.cache = get_redis_cache()
    
    def list_categories(self) -> list[CategorySchema]:

        cached_cats = self.cache.get(settings.cached_category_key)

        if cached_cats is not None:
            return [CategorySchema.model_validate(cat) for cat in cached_cats]
        
        cats_orm = self.cat_repository.get_all()

        cats_read = [CategorySchema.model_validate(cat) for cat in cats_orm]
        cats_for_cache = [cat.model_dump() for cat in cats_read]
        self.cache.set(settings.cached_category_key, cats_for_cache)

        return cats_read
    
    def create_category(self, create_cat: CategoryCreateSchema) -> CategorySchema:

        self.cache.delete(settings.cached_category_key)

        cat_orm = self.cat_repository.create_cat(name=create_cat.name)

        self.db.commit()
        self.db.refresh(cat_orm)

        return CategorySchema.model_validate(cat_orm)
    
    def update_category(self, cat_id: str, catupdate_cat: CategoryUpdateSchema) -> CategorySchema:

        cat_for_update = self.cat_repository.get_by_id(cat_id)

        if not cat_for_update:
            raise CategoryNotFound('Category not found')

        if catupdate_cat.name is not None:
            cat_for_update.name = catupdate_cat.name

        self.db.commit()
        self.db.refresh(cat_for_update)

        self.cache.delete(settings.cached_category_key)

        return CategorySchema.model_validate(cat_for_update)
    
    def delete_category(self, cat_id: str) -> None:

        cat_for_delete = self.cat_repository.get_by_id(cat_id)

        if not cat_for_delete:
            raise CategoryNotFound('Category not found')
        
        self.cat_repository.delete_cat(cat_for_delete)

        self.db.commit()

        self.cache.delete(settings.cached_category_key)
