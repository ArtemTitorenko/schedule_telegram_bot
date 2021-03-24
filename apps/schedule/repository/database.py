import asyncio

from apps.users.models import Role
from apps.users.repository.orm_models import UserOrm
from .orm_models import StudentOrm, TeacherOrm, \
        pydantic_student_creator, pydantic_teacher_creator
from ..models import Student, Teacher


async def get_student_by_id(id: int) -> Student:
    student_orm = await StudentOrm.filter(
            user__id=id, user__role=Role.student).first()
    if not student_orm:
        return None
    student = await pydantic_student_creator.from_tortoise_orm(
            student_orm)
    return Student(**student.dict())


async def get_teacher_by_id(id: int) -> Teacher:
    teacher_orm = await TeacherOrm.filter(
            user__id=id, user__role=Role.teacher).first()
    if not teacher_orm:
        return None
    teacher = await pydantic_teacher_creator.from_tortoise_orm(
            teacher_orm)
    return Teacher(**teacher.dict())

