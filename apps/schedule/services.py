import datetime

from apps.users.models import Role, User
from apps.users.repository.database import get_user_by_id

from .models import WeekSchedule, Student, Teacher
from .repository.database import get_teacher_by_id, get_student_by_id
from .repository import rest


async def get_user_week_schedule(
        user_id: int, date: datetime.date) -> WeekSchedule:
    user = await get_user_by_id(user_id)
    users_schedule_getters = {
        Role.student: _student_schedule_getter,
        Role.teacher: _teacher_schedule_getter,
    }
    return await users_schedule_getters[user.role](user, date)


async def _teacher_schedule_getter(
        user: User, date: datetime.date) -> WeekSchedule:
    teacher = await get_teacher_by_id(user.id)
    return await get_teacher_week_schedule(teacher, date)


async def _student_schedule_getter(
        user: User, date: datetime.date) -> WeekSchedule:
    student = await get_student_by_id(user.id)
    return await get_student_week_schedule(student, date)


async def get_student_week_schedule(
        student: Student, date: datetime.date) -> WeekSchedule:
    return await rest.get_group_week_schedule(
            student.group_id, date, student.specialization_id)


async def get_teacher_week_schedule(
        teacher: Teacher, date: datetime.date) -> WeekSchedule:
    return await rest.get_teacher_week_schedule(teacher.code, date)

