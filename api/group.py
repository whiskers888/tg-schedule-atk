from api.schedule import Lesson


class Group:
    def __init__(self, id, name, schedule={}):
        self.id = id
        self.name = name
        self.lessons = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
        }

    def add_schedule(self, date, lessons: Lesson):
        self.lessons[date.strftime("%A")].append(lessons)
