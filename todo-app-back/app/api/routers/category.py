from fastapi import APIRouter, Depends, status, HTTPException
from app.api.dependencies import get_cat_service
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema
from app.services.category import CategoryService, CategoryNotFound


cat_router = APIRouter(prefix='/categories')

@cat_router.get('')
async def read_categories(cat_service: CategoryService = Depends(get_cat_service)) -> list[CategorySchema]:
    return await cat_service.list_categories()

@cat_router.post('', status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreateSchema, cat_service: CategoryService = Depends(get_cat_service)) -> CategorySchema:
    return await cat_service.create_category(create_cat=payload)

@cat_router.patch('/{cat_id}')
async def update_cat(cat_id: str, payload: CategoryUpdateSchema, cat_service: CategoryService = Depends(get_cat_service)) -> CategorySchema:
    try:
        return await cat_service.update_category(cat_id=cat_id, catupdate_cat=payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
@cat_router.delete('/{cat_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: str, cat_service: CategoryService = Depends(get_cat_service)) -> None:
    try:
        await cat_service.delete_category(cat_id=cat_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")