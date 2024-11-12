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
async def check_token(token: str):
    result = await UserRepository.check_user_token({
        "token": token,
    })
    return result


@router.post("/login")
async def user_login(login: str, password: str):
    result = await UserRepository.user_login({
        "login": login,
        "password": password
    })
    return result


@router.post("/register")
async def user_register(login: str, password: str):
    result = await UserRepository.user_register({
        "login": login,
        "password": password
    })
    return result


@router.post("/change/login")
async def user_change_login(user_id: int, token: str, current_password:str, new_value:str):
    result = await UserRepository.user_change_login({
        "user_id": user_id,
        "token": token,
        "current_password": current_password,
        "new_value": new_value
    })
    return result


@router.post("/change/password")
async def user_change_password(user_id: int, token: str, current_password:str, new_value:str):
    result = await UserRepository.user_change_password({
        "user_id": user_id,
        "token": token,
        "current_password": current_password,
        "new_value": new_value
    })
    return result
