from fastapi import APIRouter

from models.task import TaskNew, TaskNewState, TaskID, TaskNewDescription, TaskNewName, TaskNewCategory
from models.user import UserToken
from repositories.task import TasksRepository


router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"]
)


@router.post("")
async def get_tasks(user_id: int, token: str):
    result = await TasksRepository.get_tasks({
        "user_id": user_id,
        "token": token,
    })
    return result


@router.post("/add")
async def add_task(user_id: int, token: str, name: str, date: str, date_time: int, description: str | None = None, category_id: int | None = None,):
    result = await TasksRepository.add_task({
        "user_id": user_id,
        "token": token,
        "name": name,
        "date": date,
        "date_time": date_time,
        "category_id": category_id,
        "description": description
    })
    return result


@router.post("/check")
async def check_task(user_id: int, token: str, task_id: int, new_value: bool):
    result = await TasksRepository.check_task({
        "user_id": user_id,
        "token": token,
        "task_id": task_id,
        "new_value": new_value
    })
    return result


@router.post("/archive")
async def archive_task(user_id: int, token: str, task_id: int):
    result = await TasksRepository.archive_task({
        "user_id": user_id,
        "token": token,
        "task_id": task_id
    })
    return result


@router.post("/delete")
async def delete_task(user_id: int, token: str, task_id: int):
    result = await TasksRepository.delete_task({
        "user_id": user_id,
        "token": token,
        "task_id": task_id
    })
    return result


@router.post("/description")
async def description_task(user_id: int, token: str, task_id: int, description: str | None = None):
    result = await TasksRepository.description_task({
        "user_id": user_id,
        "token": token,
        "task_id": task_id,
        "description": description
    })
    return result


@router.post("/rename")
async def rename_task(user_id: int, token: str, task_id: int, new_name: str):
    result = await TasksRepository.rename_task({
        "user_id": user_id,
        "token": token,
        "task_id": task_id,
        "new_name": new_name
    })
    return result


@router.post("/retype")
async def retype_task(user_id: int, token: str, task_id: int, new_category: str | None = None):
    result = await TasksRepository.retype_task({
        "user_id": user_id,
        "token": token,
        "task_id": task_id,
        "new_category": new_category
    })
    return result
