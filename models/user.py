from pydantic import BaseModel


class UserID(BaseModel):
    user_id: int


class UserToken(UserID):
    token: str


class UserModel(BaseModel):
    login: str
    password: str


class UserChange(UserToken):
    current_password: str
    new_value: str
