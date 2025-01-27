from db import async_session
from db import Positions
from sqlalchemy import select, update, delete


async def set_user(tg_id, first_name, index, username):
    async with async_session() as session:
        user = await session.scalar(select(Positions).where(Positions.tg_id == tg_id))
        if user:
            return True
        if not user:
            session.add(Positions(tg_id=tg_id, first_name=first_name, id=index, username=username))
            await session.commit()


async def check_unique_position(index):
    all_categories = await get_positions()
    for position in all_categories:
        if int(position.id) == int(index):
            return False
    return True


async def get_positions():
    async with async_session() as session:
        return await session.scalars(select(Positions))


async def delete_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Positions).where(Positions.tg_id == tg_id))
        if user:
            await session.delete(user)
            await session.commit()
        if not user:
            return 0


async def check_role(tg_id, role_name: str):
    async with async_session() as session:
        user = await session.scalar(select(Positions).where(Positions.tg_id == tg_id))
        if user.role != role_name:
            return False
        else:
            return True


async def set_role(tg_id, role_name: str):
    async with async_session() as session:
        user = await session.scalar(select(Positions).where(Positions.tg_id == tg_id))
        user.role = role_name
        await session.commit()


async def get_user(position):
    async with async_session() as session:
        user = await session.scalar(select(Positions).where(Positions.id == position))
        if user:
            return user
        if not user:
            return False


async def delete_user_by_position(position):
    async with async_session() as session:
        user = await get_user(position)
        if user:
            await session.delete(user)
            await session.commit()
        else:
            return False


async def clear_charge():
    async with async_session() as session:
        all_positions = await session.scalars(select(Positions))
        for position in all_positions:
            await session.delete(position)
        await session.commit()
