import asyncio
import typing

from apps.users.models import Role
from apps.users.repository.orm_models import UserOrm

from .orm_models import FacultyOrm, GroupOrm, SpecializationOrm
from .orm_models import pydantic_faculty_creator, pydantic_group_creator, \
        pydantic_specialization_creator
from .orm_models import StudentOrm, TeacherOrm, \
        pydantic_student_creator, pydantic_teacher_creator

from ..models import Student, Teacher
from ..models import Faculty, Group, Specialization


async def get_student_by_id(user_id: int) -> Student:
    student_orm = await StudentOrm.filter(
            user__id=id, user__role=Role.student).first()
    if not student_orm:
        return None
    student = await pydantic_student_creator.from_tortoise_orm(
            student_orm)
    return Student(**student.dict())


async def get_teacher_by_id(user_id: int) -> Teacher:
    teacher_orm = await TeacherOrm.filter(
            user__id=id, user__role=Role.teacher).first()
    if not teacher_orm:
        return None
    teacher = await pydantic_teacher_creator.from_tortoise_orm(
            teacher_orm)
    return Teacher(**teacher.dict())


async def get_faculties() -> typing.List[Faculty]:
    faculties_orm = await FacultyOrm.all()
    faculties = []
    for faculty_orm in faculties_orm:
        faculty = await pydantic_faculty_creator.from_tortoise_orm(
                faculty_orm)
        faculties.append(Faculty(**faculty.dict()))
        pass
    return faculties


async def get_faculty_by_id(faculty_id: int) -> Faculty:
    faculty_orm = await FacultyOrm.filter(id=faculty_id).first()
    faculty = await pydantic_faculty_creator.from_tortoise_orm(
            faculty_orm)
    return Faculty(**faculty.dict())


async def get_group_specializations(
        group_id: int) -> typing.List[Specialization]:
    group_orm = await GroupOrm.filter(id=group_id).first()
    specializations_orm = await group_orm.specializations.all()
    specializations = []
    for spec_orm in specializations_orm:
        spec = await pydantic_specialization_creator.from_tortoise_orm(
                spec_orm)
        specializations.append(Specialization(**spec.dict()))
    return specializations


async def get_faculty_groups(faculty_id: int) -> typing.List[Group]:
    groups_orm = await GroupOrm.filter(faculty_id=faculty_id).all()
    groups = []
    for group_orm in groups_orm:
        group = await pydantic_group_creator.from_tortoise_orm(
                group_orm)
        groups.append(Group(**group.dict()))
    return groups


async def get_groups() -> typing.List[Group]:
    groups_orm = await GroupOrm.all()
    groups = []
    for group_orm in groups_orm:
        group = await pydantic_group_creator.from_tortoise_orm(
                group_orm)
        groups.append(Group(**group.dict()))
    return groups


async def get_group_by_code(code: str) -> typing.Union[None, Group]:
    group_orm = await GroupOrm.filter(code=code).first()
    group = await pydantic_group_creator.from_tortoise_orm(group_orm)
    return Group(**group.dict())


async def get_group_by_id(group_id: int) -> Group:
    group_orm = await GroupOrm.filter(id=group_id).first()
    group = await pydantic_group_creator.from_tortoise_orm(group_orm)
    return Group(**group.dict())

