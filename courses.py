import json
from datetime import datetime
from typing import Any, List, Dict

import bs4
import requests

from cache import Cache
from school_types import Lesson, School


def same_date(date_one, date_two):
    return date_one.day == date_two.day and date_one.month == date_two.month and date_one.year == date_two.year


@Cache
def get_courses() -> List[School]:
    html = requests.get('https://orarilezioni.unicam.it/').text
    soup = bs4.BeautifulSoup(html, features="html.parser")
    courses = soup.find(id='selectPercorsi')
    groups = courses.findChildren('optgroup')
    courses_dict = {}
    for group in groups:
        courses_dict[group['label']] = {}
        courses = group.findChildren()
        for course in courses:
            courses_dict[group['label']][course.decode_contents()] = course['value']
    return [School(name, d) for name, d in courses_dict.items()]


@Cache
def get_timetable(course_id: str, course_year: str) -> List[Lesson]:
    url = f'https://unifare.unicam.it//controller/ajaxController.php?filename=..%2Fdidattica%2Fcontroller%2Forari.php' \
          f'&class=OrariController&method=getDateLezioniByPercorsoCalendar&parametri%5B%5D={course_id}&parametri%5B%5D' \
          f'=false&parametri%5B%5D={course_year}'
    text = requests.get(url).text
    courses: List[Dict[str, Any]] = json.loads(text[text.index('['):])
    now = datetime.now()
    now = datetime.strptime('2021-9-27', '%Y-%m-%d')
    courses = list(
        filter(lambda lesson: same_date(datetime.strptime(lesson['tester'].split(' ')[0], '%Y-%m-%d'), now), courses))
    return [Lesson(d) for d in courses]
