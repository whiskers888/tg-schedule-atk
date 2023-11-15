import datetime


class Lesson:
    def __init__(
        self,
        id: int,
        name: str,
        aud: str,
        teacher: str,
        date: datetime,
        start: str,
        end: str,
    ):
        self.id = id
        self.name = name
        self.aud = aud
        self.type = type
        self.teacher = teacher
        self.date = date
        self.start = start
        self.end = end
