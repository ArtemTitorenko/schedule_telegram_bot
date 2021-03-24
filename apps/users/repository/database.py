import asyncio

from .orm_models import UserOrm, pydantic_user_creator
from ..models import User


async def get_user_by_id(id: int) -> User:
    user_orm = await UserOrm.filter(id=id).first()
    if not user_orm:
        return None
    user = await pydantic_user_creator.from_tortoise_orm(user_orm)
    return User(**user.dict())

