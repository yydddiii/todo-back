import secrets

from sqlalchemy import select, delete

from models.category import ValueCategory, IDCategory, NewNameCategory
from models.user import UserToken
from database import new_session, CategoriesOrm, TasksOrm
from repositories.user import UserRepository


class CategoriesRepository:
    @classmethod
    async def get_categoies(cls, data: UserToken):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(CategoriesOrm).where(CategoriesOrm.user_id == data["user_id"])
            result = await session.execute(query)
            all_categories = result.scalars().all()

            return {"code": 200, "status": "ok", "data": all_categories}

    @classmethod
    async def add_category(cls, data: ValueCategory):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(CategoriesOrm).where(CategoriesOrm.user_id == data["user_id"])
            result = await session.execute(query)
            all_categories = result.scalars().all()

            if len(all_categories) >= 5:
                return {"code": 423, "status": "locked", "message": "Достигнуто максимальное количество категорий"}

            for item in all_categories:
                if item.name == data["value"]:
                    return {"code": 423, "status": "locked", "message": "Это имя категории уже занято"}

            new_category = CategoriesOrm(name=data["value"], user_id=data["user_id"])
            session.add(new_category)

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok", "data": new_category}

    @classmethod
    async def delete_category(cls, data: IDCategory):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = delete(CategoriesOrm).where(CategoriesOrm.id == data["category_id"])
            await session.execute(query)

            query = select(TasksOrm).where(TasksOrm.category_id == data["category_id"])
            result = await session.execute(query)
            tasks = result.scalars().all()

            for item in tasks:
                item.user_id = None

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok"}

    @classmethod
    async def rename_category(cls, data: NewNameCategory):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(CategoriesOrm).where(CategoriesOrm.id == data["category_id"])
            result = await session.execute(query)
            category = result.scalars().first()

            if category is None:
                return {"code": 404, "status": "not found"}

            query = select(CategoriesOrm).where(CategoriesOrm.user_id == data["user_id"])
            result_all = await session.execute(query)
            all_categories = result_all.scalars().all()

            for item in all_categories:
                if item.name == data["new_value"]:
                    return {"code": 423, "status": "locked", "message": "Это имя категории уже занято"}

            category.name = data["new_value"]

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok", "data": category}
