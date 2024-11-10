from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///main.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# модели таблиц
class TasksOrm(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_archived: Mapped[bool]
    is_checked: Mapped[bool]
    date: Mapped[str]
    user_id: Mapped[int]
    date_time: Mapped[int]
    category_id: Mapped[int | None]
    description: Mapped[str | None]


class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password: Mapped[str]
    token: Mapped[str | None]


class CategoriesOrm(Base):
    __tablename__ = "types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)