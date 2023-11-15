import datetime
import locale
from schedule import Schedule


class Group:
    def __init__(self, id, name, schedule={}):
        self.id = id
        self.name = name
        self.schedule = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
        }

    def add_schedule(self, date, lessons: Schedule):
        self.schedule[date.strftime("%A")].append(lessons)
