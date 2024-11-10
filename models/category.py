from models.user import UserToken


class ValueCategory(UserToken):
    value: str


class IDCategory(UserToken):
    category_id: int


class NewNameCategory(IDCategory):
    new_value: str
