import datetime
import typing

from apps.users.models import User
from pydantic import BaseModel, Field


def to_camel_case(string: str) -> str:
    first_word, *other_words = string.split('_')
    tmp = [first_word]
    for word in other_words:
        tmp.append(word.capitalize())
    return ''.join(tmp)


class Student(BaseModel):
    user: User
    group_id: int
    specialization_id: int = None


class Teacher(BaseModel):
    user: User
    code: str


class Day(BaseModel):
    date: str
    is_study_day: bool
    weekday_number: int

    class Config:
        fields = {'weekday_number': 'weekDayNumber'}
        alias_generator = to_camel_case


class Week(BaseModel):
    type: str
    number: int
    days: typing.List[Day]


class Lesson(BaseModel):
    type: str
    is_canceled: bool
    is_moved: bool
    rooms: typing.List[str]
    course_name: str
    time_chunks: typing.List[str]
    teachers: typing.List[str]


class DaySchedule(BaseModel):
    lessons: typing.List[Lesson] = Field(default_factory=list)


class WeekSchedule(BaseModel):
    week: Week
    schedule: typing.List[DaySchedule]

