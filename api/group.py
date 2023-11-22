from api.schedule import Lesson


class Group:
    def __init__(self, id, name, course, schedule={}):
        self.id = id
        self.name = name
        self.course = course
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

    def lessons_clear(self):
        self.lessons = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
        }
