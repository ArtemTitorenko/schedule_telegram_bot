import os

from apps.users.repository.orm_models import UserOrm

from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class StudentOrm(Model):
    user: fields.OneToOneRelation[UserOrm] = fields.OneToOneField(
            model_name='users.UserOrm',
            related_name='student',
            on_delete=fields.CASCADE)

    group_id = fields.IntField()
    specialization_id = fields.IntField(null=True)

    class Meta:
        app = 'schedule'
        table = 'students'


class TeacherOrm(Model):
    user: fields.OneToOneRelation[UserOrm] = fields.OneToOneField(
            model_name='users.UserOrm',
            related_name='teacher',
            on_delete=fields.CASCADE)

    code = fields.CharField(50)

    class Meta:
        app = 'schedule'
        table = 'teachers'

Tortoise.init_models(['apps.schedule.repository.orm_models'], 'schedule')
pydantic_student_creator = pydantic_model_creator(StudentOrm)
pydantic_teacher_creator = pydantic_model_creator(TeacherOrm)

