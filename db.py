import datetime

from sqlalchemy import BigInteger, String, ForeignKey, DATE
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL)

async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class Positions(Base):
    __tablename__ = 'positions'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(default="NULL")
    role: Mapped[str] = mapped_column(default="user")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



