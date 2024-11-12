import secrets

from sqlalchemy import select, delete

from database import new_session, UsersOrm
from models.user import UserID, UserModel, UserToken, UserChange


class UserRepository:
    @classmethod
    async def get_all_users(cls):
        async with new_session() as session:
            query = select(UsersOrm)
            result = await session.execute(query)
            all_users = result.scalars().all()

            return all_users

    @classmethod
    async def delete_user(cls, select_id: UserID):
        async with new_session() as session:
            query = delete(UsersOrm).where(UsersOrm.id == select_id.user_id)
            result = await session.execute(query)

            await session.flush()
            await session.commit()

            return result

    @classmethod
    async def check_user_token(cls, select_token: UserToken):
        async with new_session() as session:
            query = select(UsersOrm).where(UsersOrm.token == select_token["token"])
            result = await session.execute(query)
            select_user = result.scalars().first()

            if select_user is None:
                return {"code": 403, "status": "forbidden"}

            return {"code": 200, "status": "ok", "data": {"user_id": select_user.id, "user_login": select_user.login}}

    @classmethod
    async def user_login(cls, data: UserModel):
        async with new_session() as session:
            query = select(UsersOrm).where(UsersOrm.login == data["login"])
            result = await session.execute(query)
            select_user = result.scalars().first()

            if select_user is None:
                return {"code": 403, "status": "forbidden", "message": "Пользователь не найден"}

            if select_user.password != data["password"]:
                return {"code": 403, "status": "forbidden", "message": "Пароль не верный"}

            select_user.token = secrets.token_hex(16)

            await session.flush()
            await session.commit()

            return {"code": 200, "staus": "ok", "data": {"token": select_user.token}}

    @classmethod
    async def user_register(cls, data: UserModel):
        async with new_session() as session:
            query = select(UsersOrm).where(UsersOrm.login == data["login"])
            result = await session.execute(query)
            select_user = result.scalars().first()

            if select_user is not None:
                return {"code": 403, "status": "forbidden", "message": "Логин уже занят"}

            new_user = UsersOrm(login=data["login"], password=data["password"], token=secrets.token_hex(16))
            session.add(new_user)

            await session.flush()
            await session.commit()

            return {"code": 200, "staus": "ok", "data": {"token": new_user.token}}

    @classmethod
    async def user_change_login(cls, data: UserChange):
        async with new_session() as session:
            query = select(UsersOrm).where(UsersOrm.id == data["user_id"])
            result = await session.execute(query)
            select_user = result.scalars().first()

            query = select(UsersOrm).where(UsersOrm.login == data["new_value"])
            result = await session.execute(query)
            select_login = result.scalars().first()

            if select_user is None or data["current_password"] != select_user.password or data["token"] != select_user.token:
                return {"code": 403, "status": "forbidden", "message": "Доступ запрещен"}

            if select_login is not None:
                return {"code": 403, "status": "forbidden", "message": "Логин уже занят"}

            select_user.login = data["new_value"]

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok", "message": "Логин успешно изменен", "data": {
                "new_login": select_user.login
            }}

    @classmethod
    async def user_change_password(cls, data: UserChange):
        async with new_session() as session:
            query = select(UsersOrm).where(UsersOrm.id == data["user_id"])
            result = await session.execute(query)
            select_user = result.scalars().first()

            if select_user is None or data["current_password"] != select_user.password or data["token"] != select_user.token:
                return {"code": 403, "status": "forbidden", "message": "Доступ запрещен"}

            if select_user.password == data["new_value"]:
                return {"code": 403, "status": "forbidden", "message": "Пароли не должны совпадать"}

            select_user.password = data["new_value"]

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok", "message": "Пароль успешно изменен"}
