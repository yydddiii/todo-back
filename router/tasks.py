from fastapi import APIRouter

from models.task import TaskNew, TaskNewState, TaskID, TaskNewDescription, TaskNewName, TaskNewCategory
from models.user import UserToken
from repositories.task import TasksRepository


router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"]
)


@router.post("")
async def get_tasks(data: UserToken):
    result = await TasksRepository.get_tasks(data)
    return result


@router.post("/add")
async def add_task(data: TaskNew):
    result = await TasksRepository.add_task(data)
    return result


@router.post("/check")
async def check_task(data: TaskNewState):
    result = await TasksRepository.check_task(data)
    return result


@router.post("/archive")
async def archive_task(data: TaskID):
    result = await TasksRepository.archive_task(data)
    return result


@router.post("/delete")
async def delete_task(data: TaskID):
    result = await TasksRepository.delete_task(data)
    return result


@router.post("/description")
async def description_task(data: TaskNewDescription):
    result = await TasksRepository.description_task(data)
    return result


@router.post("/rename")
async def rename_task(data: TaskNewName):
    result = await TasksRepository.rename_task(data)
    return result


@router.post("/retype")
async def retype_task(data: TaskNewCategory):
    result = await TasksRepository.retype_task(data)
    return result
