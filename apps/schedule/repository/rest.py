import aiohttp
import datetime
import pytz
import typing

from pydantic import BaseModel
from pydantic import parse_obj_as

#from ..models import Faculty, Group, Specialization
from ..models import Day, Week, Lesson, DaySchedule, WeekSchedule


DATE_FORMAT = '%d-%m-%Y'
API_URL = 'https://lk.gubkin.ru/schedule/api/api.php'


async def get_group_week_schedule(group_id: int,
                                  date: datetime.date,
                                  spec_id: int = None) -> WeekSchedule:
    params = {
        'date': _convert_date_to_str(date),
        'groupId': str(group_id),
        'act': 'schedule',
    }

    if spec_id:
        params['difId'] = difId

    json_response = await _get_json_response(params)
    return _parse_schedule(json_response)


async def get_teacher_week_schedule(teacher_id: str,
                                    date: datetime.date) -> WeekSchedule:
    params = {
        'date': _convert_date_to_str(date),
        'teacherId': str(teacher_id),
        'act': 'schedule',
    }

    json_response = await _get_json_response(params)
    return _parse_schedule(json_response)


async def _get_json_response(params: dict) -> dict:
    session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False))
    async with session.get(API_URL, params=params) as response:
        json_response = await response.json()
    await session.close()
    return json_response


def _parse_schedule(response: dict) -> WeekSchedule:
    schedule_data = response['rows']

    week_russia = Week(**schedule_data['week']['weekRussia'])
    lessons = _parse_lessons(schedule_data)
    schedule = _combining_lessons_by_days(lessons, week_russia)

    return WeekSchedule(week=week_russia, schedule=schedule)


def _convert_date_to_str(date: datetime.date) -> str:
    return date.strftime(DATE_FORMAT)


def _convert_str_to_date(date: str) -> datetime.date:
    return datetime.datetime.strptime(date, DATE_FORMAT).date()


def _parse_lessons(schedule_data: dict) -> typing.List[Lesson]:
    moscow_organization = schedule_data['organizations'][0]
    raw_lessons = moscow_organization['lessons']
    time_chunks = moscow_organization['lessonsTimeChunks']

    lessons = parse_obj_as(typing.List[Lesson], raw_lessons)
    _convert_time_chunks(lessons, time_chunks)

    return lessons


def _convert_time_chunks(lessons: typing.List[Lesson],
                         time_chunks: typing.List[str]) -> None:
    for lesson in lessons:
        tmp = []
        for chunk in lesson.time_chunks:
            tmp.append(time_chunks[int(chunk)])
        lesson.time_chunks = tmp


def _combining_lessons_by_days(lessons: typing.List[Lesson],
                               week: Week) -> typing.List[DaySchedule]:

    days_schedule = [[] for _ in range(7)]
    for lesson in lessons:
        days_schedule[lesson.weekday_number].append(lesson)

    schedule = []
    for day_lessons in days_schedule:
        schedule.append(DaySchedule(lessons=day_lessons))

    return schedule

