import os

import json
import requests
from datetime import datetime, timedelta

def same_date(date_one, date_two):
    return date_one.day == date_two.day and date_one.month == date_two.month and date_one.year == date_two.year

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    course = 10028
    course_year = 0


    url = f'https://unifare.unicam.it//controller/ajaxController.php?filename=..%2Fdidattica%2Fcontroller%2Forari.php' \
          f'&class=OrariController&method=getDateLezioniByPercorsoCalendar&parametri%5B%5D={course}&parametri%5B%5D' \
          f'=false&parametri%5B%5D={course_year}'

    text = requests.get(url).text

    courses = json.loads(text[text.index('['):])

    # now = datetime.now()
    now = datetime.strptime('2021-9-20', '%Y-%m-%d')
    courses = list(filter(lambda lesson: same_date(datetime.strptime(lesson['tester'].split(' ')[0], '%Y-%m-%d'), now), courses))
    print(json.dumps(courses, indent=4, sort_keys=True))
