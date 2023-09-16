import json
from app.utils.stats import UsersUsage
from app.db import database
from app.v2ray.v2call import VMessUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.tables import Users
from collections.abc import AsyncIterator
from sqlalchemy import select, update
from v2client.v2ray import stats


async def get_user(email: str) -> Users | bool:
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        query = select(Users).where(Users.email == email)
        result = await session.execute(query)
        if user := result.scalars().first():
            return user
        else:
            return False


async def get_session():
    async_iterator: AsyncIterator[AsyncSession] = database.session()
    return await anext(async_iterator)


async def db_add_vmess_user(user: VMessUser) -> None:
    async_session: AsyncSession = await get_session()
    protocol_detail = str(json.dumps(vars(user)))
    async with async_session.__call__() as session:
        async with session.begin():
            session.add(Users(
                email=user.email, uuid=user.userUuid, active=True, protocol="vmess", protocol_detail=protocol_detail
            ))


async def db_add_vless_user(email: str):
    pass


async def db_add_trojan_user():
    pass


async def db_remove_user(email: str) -> bool:
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        if user := await get_user(email=email):
            await session.delete(user)
            await session.commit()
            return True
        else:
            return False


async def db_update_activity(email: str, active: bool) -> Users | bool:
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        if user := await get_user(email=email):
            user.active = active
            # user_dict = vars(user)
            # user_dict.pop("_sa_instance_state")
            # query = update(Users).values(user_dict).where(Users.id == user.id)
            query = update(Users).values({"active": active}).where(Users.id == user.id)
            await session.execute(query)
            await session.commit()
            return user
        else:
            return False


async def db_user_usage(email: str) -> stats.UsageResponse | bool:
    if user := await get_user(email=email):
        return stats.UsageResponse(user.download, user.upload)
    else:
        return False


async def db_users_usage() -> list | bool:
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        query = select(Users).order_by(Users.id)
        result = await session.execute(query)
        if users := result.scalars().all():
            list_user_usage = list()
            for user in users:
                list_user_usage.append(
                    UsersUsage(email=user.email, upload=float(user.upload), download=float(user.download))
                )
            return list_user_usage
        else:
            return False


def db_traffic_all():
    pass
