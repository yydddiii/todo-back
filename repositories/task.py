from sqlalchemy import select, delete

from models.task import TaskNew, TaskNewState, TaskID, TaskNewDescription, TaskNewName, TaskNewCategory
from models.user import UserToken
from database import new_session, TasksOrm, CategoriesOrm
from repositories.user import UserRepository


class TasksRepository:
    @classmethod
    async def get_tasks(cls, data: UserToken):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(TasksOrm).where(TasksOrm.user_id == data.user_id)
            result = await session.execute(query)
            all_tasks = result.scalars().all()

            return {"code": 200, "status": "ok", "data": all_tasks}

    @classmethod
    async def add_task(cls, data: TaskNew):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            new_task = TasksOrm(
                name=data.name,
                is_archived=False,
                is_checked=False,
                date=data.date,
                user_id=data.user_id,
                date_time=data.date_time,
                category_id=data.category_id,
                description=data.description
            )
            session.add(new_task)

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok", "data": new_task}

    @classmethod
    async def check_task(cls, data: TaskNewState):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(TasksOrm).where(TasksOrm.id == data.task_id)
            result = await session.execute(query)
            task = result.scalars().first()

            if task == None:
                return {"code": 404, "status": "not found"}

            if task.is_checked == data.new_value:
                return {"code": 208, "status": "already reported"}

            task.is_checked = data.new_value

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok"}

    @classmethod
    async def archive_task(cls, data: TaskID):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(TasksOrm).where(TasksOrm.id == data.task_id)
            result = await session.execute(query)
            task = result.scalars().first()

            if task == None:
                return {"code": 404, "status": "not found"}

            if task.is_archived:
                task.is_archived = False
            else:
                task.is_archived = True

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok"}

    @classmethod
    async def delete_task(cls, data: TaskID):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = delete(TasksOrm).where(TasksOrm.id == data.task_id)
            await session.execute(query)

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok"}

    @classmethod
    async def description_task(cls, data: TaskNewDescription):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(TasksOrm).where(TasksOrm.id == data.task_id)
            result = await session.execute(query)
            task = result.scalars().first()

            if task == None:
                return {"code": 404, "status": "not found"}

            task.description = data.description

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok"}

    @classmethod
    async def rename_task(cls, data: TaskNewName):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(TasksOrm).where(TasksOrm.id == data.task_id)
            result = await session.execute(query)
            task = result.scalars().first()

            if task == None:
                return {"code": 404, "status": "not found"}

            task.name = data.new_name

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok"}

    @classmethod
    async def retype_task(cls, data: TaskNewCategory):
        async with new_session() as session:
            access_token = await UserRepository.check_user_token(data)

            if access_token['code'] != 200:
                return access_token

            query = select(TasksOrm).where(TasksOrm.id == data.task_id)
            result = await session.execute(query)
            task = result.scalars().first()

            if task == None:
                return {"code": 404, "status": "not found"}

            if data.new_category != None:
                query = select(CategoriesOrm).where(CategoriesOrm.id == data.new_category)
                result = await session.execute(query)
                category = result.scalars().first()

                if category == None:
                    return {"code": 404, "status": "not found"}

            task.category_id = data.new_category

            await session.flush()
            await session.commit()

            return {"code": 200, "status": "ok"}
