from homeassistant.helpers.entity import Entity
import json
from vulcan import Vulcan
import asyncio
import datetime
from datetime import timedelta
from homeassistant.helpers import config_validation as cv, entity_platform, service
from .const import (
    CONF_STUDENT_NAME,
)
from .__init__ import client
from . import DOMAIN


def get_lesson_info(self, days_to_add=0):
    self.lesson_1 = {}
    self.lesson_2 = {}
    self.lesson_3 = {}
    self.lesson_4 = {}
    self.lesson_5 = {}
    self.lesson_6 = {}
    self.lesson_7 = {}
    self.lesson_8 = {}
    self.lesson_9 = {}
    self.lesson_10 = {}

    for Lesson in client.get_lessons(
        datetime.date.today() + timedelta(days=days_to_add)
    ):
        temp_dict = {}
        temp_dict["number"] = Lesson.number
        lesson = str(Lesson.number)
        temp_dict["lesson"] = Lesson.subject.name
        temp_dict["room"] = Lesson.room
        temp_dict["visible"] = Lesson.visible
        temp_dict["changes"] = Lesson.changes
        temp_dict["group"] = Lesson.group
        temp_dict["teacher"] = Lesson.teacher.name
        temp_dict["time"] = (
            Lesson.time.from_.strftime("%H:%M") + "-" + Lesson.time.to.strftime("%H:%M")
        )
        if "przeniesiona na lekcję" in temp_dict["changes"]:
            temp_dict["lesson"] = "Lekcja przeniesiona (" + temp_dict["lesson"] + ")"
        elif "przeniesiona z lekcji" in temp_dict["changes"]:
            temp_dict["lesson"] = temp_dict["lesson"] + " " + temp_dict["changes"]
        elif (
            "odwołana" in temp_dict["changes"]
            or "Okienko" in temp_dict["changes"]
            or "nieobecność" in temp_dict["changes"]
            or "okienko" in temp_dict["changes"]
        ):
            temp_dict["lesson"] = "Lekcja odwołana (" + temp_dict["lesson"] + ")"
        if temp_dict["visible"] == True:
            setattr(self, "lesson_" + lesson, temp_dict)

    lesson_ans = {}
    if self.lesson_1 == {}:
        self.lesson_1 = {
            "number": 1,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_2 == {}:
        self.lesson_2 = {
            "number": 2,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_3 == {}:
        self.lesson_3 = {
            "number": 3,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_4 == {}:
        self.lesson_4 = {
            "number": 4,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_5 == {}:
        self.lesson_5 = {
            "number": 5,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_6 == {}:
        self.lesson_6 = {
            "number": 6,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_7 == {}:
        self.lesson_7 = {
            "number": 7,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_8 == {}:
        self.lesson_8 = {
            "number": 8,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_9 == {}:
        self.lesson_9 = {
            "number": 9,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }
    if self.lesson_10 == {}:
        self.lesson_10 = {
            "number": 10,
            "lesson": "-",
            "room": "-",
            "group": "-",
            "teacher": "-",
            "time": "-",
            "changes": "-",
        }

    i = 1
    for _ in range(10):
        dict_ans = {
            "lesson_1": self.lesson_1,
            "lesson_2": self.lesson_2,
            "lesson_3": self.lesson_3,
            "lesson_4": self.lesson_4,
            "lesson_5": self.lesson_5,
            "lesson_6": self.lesson_6,
            "lesson_7": self.lesson_7,
            "lesson_8": self.lesson_8,
            "lesson_9": self.lesson_9,
            "lesson_10": self.lesson_10,
        }
    return dict_ans


def get_student_info(student_name):
    student_info = {}
    for student in client.get_students():
        if student.name == student_name:
            id = student.id
            class_ = student.class_.name
            school = student.school.name
            name = student.name
        else:
            name = student.name
            id = student.id
            class_ = student.class_.name
            school = student.school.name
    student_info["name"] = name
    student_info["id"] = id
    student_info["class"] = class_
    student_info["school"] = school
    return student_info


def get_latest_attendance(self):
    self.latest_attendance = {}

    for attendance in client.get_attendance():
        temp_dict = {}
        if attendance.category != None:
            temp_dict["content"] = attendance.category.name
            temp_dict["lesson_name"] = attendance.subject.name
            temp_dict["lesson_number"] = attendance.time.number
            temp_dict["lesson_date"] = str(attendance.date)
            temp_dict["lesson_time"] = (
                attendance.time.from_.strftime("%H:%M")
                + "-"
                + attendance.time.to.strftime("%H:%M")
            )
            temp_dict["datetime"] = datetime.datetime.combine(
                attendance.date, attendance.time.from_
            )
        setattr(self, "latest_attendance", temp_dict)

    if self.latest_attendance == {}:
        self.latest_attendance = {
            "content": "-",
            "lesson_name": "-",
            "lesson_number": "-",
            "lesson_date": "-",
            "lesson_time": "-",
            "datetime": "-",
        }

    return self.latest_attendance


def get_latest_grade(self):
    self.latest_grade = {}

    for grade in client.get_grades():
        temp_dict = {}
        temp_dict["content"] = grade.content
        temp_dict["weight"] = grade.weight
        temp_dict["description"] = grade.description
        temp_dict["value"] = grade.value
        temp_dict["teacher"] = grade.teacher.name
        temp_dict["subject"] = grade.subject.name
        temp_dict["date"] = grade.date
        setattr(self, "latest_grade", temp_dict)

    if self.latest_grade == {}:
        self.latest_grade = {
            "content": "-",
            "date": "-",
            "weight": "-",
            "description": "-",
            "subject": "-",
            "teacher": "-",
            "value": 0,
        }

    return self.latest_grade


def get_homework(self):
    next_homework = {}
    for homework in client.get_homework(
        datetime.date.today(), datetime.date.today() + timedelta(7)
    ):
        next_homework = {}
        next_homework["description"] = homework.description
        next_homework["subject"] = homework.subject.name
        next_homework["teacher"] = homework.teacher.name
        next_homework["date"] = homework.date.strftime("%d.%m.%Y")

    if next_homework == {}:
        next_homework = {
            "description": "Brak zadań domowych",
            "subject": "w najbliższym tygodniu",
            "teacher": "-",
            "date": "-",
        }

    return next_homework


def get_exam(self):
    next_exam = {}
    for exam in client.get_exams(
        datetime.date.today(), datetime.date.today() + timedelta(7)
    ):
        next_exam = {}
        next_exam["description"] = exam.description
        next_exam["subject"] = exam.subject.name
        next_exam["type"] = exam.type.name
        next_exam["teacher"] = exam.teacher.name
        next_exam["date"] = exam.date.strftime("%d.%m.%Y")

    if next_exam["type"] == "SHORT_TEST":
        next_exam["type"] = "Kartkówka"
    elif next_exam["type"] == "CLASS_TEST":
        next_exam["type"] = "Praca Klasowa"
    elif next_exam["type"] == "EXAM":
        next_exam["type"] = "Sprawdzian"

    if next_exam == {}:
        next_exam = {
            "description": "Brak sprawdzianów",
            "subject": "w najbliższym tygodniu",
            "type": "-",
            "teacher": "-",
            "date": "-",
        }

    return next_exam


def get_latest_message(self):
    self.latest_message = {}

    for message in client.get_messages():
        temp_dict = {}
        temp_dict["title"] = message.title
        temp_dict["content"] = message.content
        if message.sender is not None:
            temp_dict["sender"] = message.sender.name
        else:
            temp_dict["sender"] = "Nieznany"
        temp_dict["date"] = (
            message.sent_date.strftime("%Y.%m.%d")
            + " "
            + message.sent_time.strftime("%H:%M")
        )
        setattr(self, "latest_message", temp_dict)

    if self.latest_message == {}:
        self.latest_message = {
            "content": "-",
            "date": "-",
            "weight": "-",
            "description": "-",
            "subkect": "-",
            "teacher": "-",
            "value": 0,
        }

    return self.latest_message
