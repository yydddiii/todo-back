from fastapi import APIRouter

from models.category import ValueCategory, IDCategory, NewNameCategory
from models.user import UserToken
from repositories.category import CategoriesRepository

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)


@router.post("")
async def get_categories(token: UserToken):
    result = await CategoriesRepository.get_categoies(token)
    return result


@router.post("/add")
async def add_category(token: ValueCategory):
    result = await CategoriesRepository.add_category(token)
    return result


@router.post("/delete")
async def delete_category(data: IDCategory):
    result = await CategoriesRepository.delete_category(data)
    return result


@router.post("/change")
async def change_category(data: NewNameCategory):
    result = await CategoriesRepository.rename_category(data)
    return result