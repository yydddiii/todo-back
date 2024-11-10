from fastapi import APIRouter

from models.user import UserModel, UserID, UserToken, UserChange
from repositories.user import UserRepository

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/all")
async def get_users():
    all_users = await UserRepository.get_all_users()
    return {"code": 200, "status": "ok", "data": all_users}


@router.post("/delete")
async def del_user(select_id: UserID):
    await UserRepository.delete_user(select_id)
    return {"code": 200, "status": "ok"}


@router.post("/ckeck_token")
async def check_token(token: UserToken):
    result = await UserRepository.check_user_token(token)
    return result


@router.post("/login")
async def user_login(data: UserModel):
    result = await UserRepository.user_login(data)
    return result


@router.post("/register")
async def user_register(data: UserModel):
    result = await UserRepository.user_register(data)
    return result


@router.post("/change/login")
async def user_change_login(data: UserChange):
    result = await UserRepository.user_change_login(data)
    return result


@router.post("/change/password")
async def user_change_password(data: UserChange):
    result = await UserRepository.user_change_password(data)
    return result
