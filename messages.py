from typing import List

from school_types import Lesson


def get_pretty_message(course: str, year: str, lessons: List[Lesson]) -> str:
    header: str = f'🎓 *{course}, {year}*\n\n'
    final_message: str = ""
    for single_lesson in lessons:
        place: str = single_lesson.description.split(" <div style=\"height:8px\"></div><b>Docenti:</b> ")[0]
        teacher: str = single_lesson.description.split(" <div style=\"height:8px\"></div><b>Docenti:</b> ")[1]
        final_message = final_message + f'🔔 *{single_lesson.title} - {single_lesson.year}° anno*\n*🧑‍ {teacher}*\n🏫 ' \
                                        f'{place}\n⏲️ _{single_lesson.tester}_\n\n\n '
    if final_message == "":
        final_message = "Non sono presenti materie per la data e facoltà selezionate."
    return header + final_message


def get_startup_message() -> str:
    return f'Benvenuto!\nScrivi /start per iniziare!'
