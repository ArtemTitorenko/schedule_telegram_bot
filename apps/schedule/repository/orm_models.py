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


class SpecializationOrm(Model):
    id = fields.IntField(pk=True, generated=False)
    name = fields.CharField(150)
    code = fields.CharField(50)
    groups: fields.ManyToManyRelation = fields.ManyToManyField(
            model_name='schedule.GroupOrm',
            related_name='specializations',
            on_delete=fields.CASCADE)

    class Meta:
        app = 'schedule'
        table = 'specializations'

    class PydanticMeta:
        exclude = ('groups',)


class GroupOrm(Model):
    id = fields.IntField(pk=True, generated=False)
    code = fields.CharField(50)
    faculty: fields.ForeignKeyRelation = fields.ForeignKeyField(
            model_name='schedule.FacultyOrm',
            related_name='groups',
            on_delete=fields.CASCADE)

    specializations: fields.ReverseRelation['SpecializationOrm']

    # tortoise ставит ограничение в модели pydantic на поле >= 1
    def faculty_id(self) -> int:
        return self.faculty_id

    class Meta:
        app = 'schedule'
        table = 'groups'

    class PydanticMeta:
        exclude = ('specializations', 'faculty', 'faculty_id')
        computed = ('faculty_id',)


class FacultyOrm(Model):
    id = fields.IntField(pk=True, generated=False)
    name = fields.CharField(150)
    code = fields.CharField(50)

    groups: fields.ReverseRelation['GroupOrm']

    class Meta:
        app = 'schedule'
        table = 'faculties'

    class PydanticMeta:
        exclude = ('groups')


Tortoise.init_models(['apps.schedule.repository.orm_models'], 'schedule')
pydantic_student_creator = pydantic_model_creator(StudentOrm)
pydantic_teacher_creator = pydantic_model_creator(TeacherOrm)
pydantic_faculty_creator = pydantic_model_creator(FacultyOrm)
pydantic_group_creator = pydantic_model_creator(GroupOrm)
pydantic_specialization_creator = pydantic_model_creator(SpecializationOrm)

