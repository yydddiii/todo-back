from fastapi import APIRouter

from models.category import ValueCategory, IDCategory, NewNameCategory
from models.user import UserToken
from repositories.category import CategoriesRepository

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)


@router.post("")
async def get_categories(user_id: int, token: str):
    result = await CategoriesRepository.get_categoies({
        "user_id": user_id,
        "token": token,
    })
    return result


@router.post("/add")
async def add_category(user_id: int, token: str, value: str):
    result = await CategoriesRepository.add_category({
        "user_id": user_id,
        "token": token,
        "value": value
    })
    return result


@router.post("/delete")
async def delete_category(user_id: int, token: str, category_id: int):
    result = await CategoriesRepository.delete_category({
        "user_id": user_id,
        "token": token,
        "category_id": category_id
    })
    return result


@router.post("/change")
async def change_category(user_id: int, token: str, category_id: int, new_value: str):
    result = await CategoriesRepository.rename_category({
        "user_id": user_id,
        "token": token,
        "category_id": category_id,
        "new_value": new_value
    })
    return result