import datetime
import typing

from apps.users.models import User
from pydantic import BaseModel, Field, conint


def to_camel_case(string: str) -> str:
    first_word, *other_words = string.split('_')
    tmp = [first_word]
    for word in other_words:
        tmp.append(word.capitalize())
    return ''.join(tmp)

#################
# schedule users
################


class Student(BaseModel):
    user: User
    group_id: int
    specialization_id: int = None


class Teacher(BaseModel):
    user: User
    code: str


################
# schedule
################


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


class TeacherParse(BaseModel):
    code: str
    first_name: str
    last_name: str
    patronymic: str

    class Config:
        fields = {'code': 'id'}
        alias_generator = to_camel_case


class Course(BaseModel):
    id: int
    name: str


class Room(BaseModel):
    id: int
    number: str


class GroupParse(BaseModel):
    id: int
    code: str
    faculty_id: int

    class Config:
        fields = {
            'faculty_id': 'facultyId'
        }


class Lesson(BaseModel):
    type: str
    is_canceled: bool
    is_moved: bool
    weekday_number: int
    time_chunks: typing.List[str]
    course: Course
    teachers: typing.List[TeacherParse]
    groups: typing.List[GroupParse]
    division_name: str

    class Config:
        fields = {'weekday_number': 'weekDayNumber'}
        alias_generator = to_camel_case


class DaySchedule(BaseModel):
    lessons: typing.List[Lesson] = Field(default_factory=list)


class WeekSchedule(BaseModel):
    week: Week
    schedule: typing.List[DaySchedule]


class Specialization(BaseModel):
    id: int
    name: str
    code: str


class Group(BaseModel):
    id: int
    code: str
    faculty_id: int = None


class Faculty(BaseModel):
    id: int
    name: str
    code: str

