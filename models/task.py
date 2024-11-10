from models.user import UserToken


class TaskNew(UserToken):
    name: str
    date: str
    date_time: int
    category_id: int | None = None
    description: str | None = None


class TaskID(UserToken):
    task_id: int


class TaskNewDescription(TaskID):
    description: str | None = None


class TaskNewName(TaskID):
    new_name: str


class TaskNewCategory(TaskID):
    new_category: int | None = None


class TaskNewState(TaskID):
    new_value: bool
