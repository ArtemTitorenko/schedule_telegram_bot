import os

from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import Role


class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class UserOrm(TimestampMixin, Model):
    # telegram_id
    id = fields.BigIntField(pk=True)
    first_name = fields.CharField(50)
    role = fields.CharEnumField(Role)
    is_admin = fields.BooleanField(default=False)
    last_name = fields.CharField(50, null=True)
    username = fields.CharField(100, null=True)

    class Meta:
        table = 'users'
        app = 'users'


Tortoise.init_models(['apps.users.repository.orm_models'], 'users')
pydantic_user_creator = pydantic_model_creator(UserOrm)

