from typing import Dict, Any, List


class Lesson(object):

    def __init__(self, d: Dict[str, Any]):
        self.id: int = d["id"]
        self.title: str = d["title"]
        self.description: str = d["description"]
        self.module_id: int = d["idModulo"]
        self.start: int = d["start"]
        self.end: int = d["end"]
        self.tester: str = d["tester"]
        self.lesson_id: int = d["idLezione"]
        self.class_name: str = d["className"]
        self.color: str = d["color"]
        self.year: int = d["anno"]


class School(object):

    def __init__(self, name: str, courses: Dict[str, str]):
        self.courses: List[Course] = []
        self.name = name
        for name, course_id in courses.items():
            self.courses.append(Course(name, course_id))


class Course(object):
    def __init__(self, name: str, course_id: str):
        self.name = name
        self.course_id = course_id
