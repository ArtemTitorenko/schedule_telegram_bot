import aiohttp
import datetime
import pytz
import typing

from pydantic import BaseModel
from pydantic import parse_obj_as

from ..models import Faculty, Group, Specialization
from ..models import Day, Week, Lesson, DaySchedule, WeekSchedule


DATE_FORMAT = '%d-%m-%Y'
API_URL = 'https://lk.gubkin.ru/schedule/api/api.php'


async def get_faculties() -> typing.List[Faculty]:
    params = {
        'act': 'list',
        'method': 'getFaculties',
    }
    json_response = await _get_json_response(params)
    return parse_obj_as(typing.List[Faculty], json_response['rows'])


async def get_faculty_by_id(faculty_id: int) -> Faculty:
    faculties = await get_faculties()
    for faculty in faculties:
        if faculty.id == faculty_id:
            return faculty


async def get_group_specializations(
        group_id: int) -> typing.List[Specialization]:
    params = {
        'act': 'list',
        'method': 'getGroupSpecializations',
        'groupId': str(group_id),
    }
    json_response = await _get_json_response(params)
    # характерность API
    if not json_response['rows'][0]['code']:
        return []
    specializations = parse_obj_as(typing.List[Specialization],
                                   json_response['rows'])
    return specializations


async def get_faculty_groups(faculty_id: int) -> typing.List[Group]:
    params = {
        'act': 'list',
        'method': 'getFacultyGroups',
        'facultyId': str(faculty_id),
    }
    json_response = await _get_json_response(params)
    groups = parse_obj_as(typing.List[Group], json_response['rows'])
    for group in groups:
        group.faculty_id = faculty_id
    return groups


async def get_groups() -> typing.List[Group]:
    all_groups = []
    faculties = await get_faculties()
    for faculty in faculties:
        faculty_groups = await get_faculty_groups(faculty.id)
        all_groups.extend(faculty_groups)
    return all_groups


async def get_group_by_code(code: str) -> typing.Union[None, Group]:
    code = code.lower()
    faculties = await get_faculties()
    for faculty in sorted(faculties,
                          key=lambda faculty: abs(ord(faculty.name.lower()[0]) - ord(code[0]))):
        faculty_groups = await get_faculty_groups(faculty.id)
        for group in faculty_groups:
            if group.code.lower() == code:
                return group


async def get_group_by_id(group_id: int) -> Group:
    groups = await get_groups()
    for group in groups:
        if group.id == group_id:
            return group


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

