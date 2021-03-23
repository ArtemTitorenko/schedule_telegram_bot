from enum import Enum, unique
from pydantic import BaseModel


@unique
class Role(str, Enum):
    student = 'student'
    teacher = 'teacher'


class User(BaseModel):
    telegram_id: int
    first_name: str
    role: Role
    is_admin: bool = False
    last_name: str = None
    user_name: str = None

