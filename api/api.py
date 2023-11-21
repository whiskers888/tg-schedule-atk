import requests
from api.url import Links
from api.group import Group
from api.schedule import Lesson
import datetime


class Dispatcher_DSTU:
    _groups = []
    _schedule = []

    def __init__(self) -> None:
        self._get_groups()

    def find_groups_by_course(self, course):
        select_groups = []

        for group in self._groups:
            if group.course == int(course):
                select_groups.append(group)

        return select_groups

    def find_schedule_by_group(self, group_id: int):
        group = self._find_group(group_id)
        return self._get_schedule(group)

    def find_group_schedule_by_day(self, group_id: int, weekday: str):
        group = self._find_group(group_id)
        self._get_schedule(group)
        return self._schedule_to_str(group, weekday)

    # Функция собирает группы
    def _collect_groups(self, raspGroupList: dict):
        for item in raspGroupList["data"]:
            if item["facul"] == "АТК":
                self._groups.append(Group(item["id"], item["name"], item["kurs"]))

    # Функция для сборки групп
    def _get_groups(self):
        params = {"year": "2023-2024"}

        response = requests.get(Links.rasp_group_list, params=params)

        if response.status_code == 200:
            self._collect_groups(response.json())
            return [group.name for group in self._groups]
        else:
            print("Произошла ошибка при выполнении запроса.")

    # Функция находит группу по ее id
    def _find_group(self, group_id: int):
        for group in self._groups:
            if group.id == group_id:
                return group

    def _collect_schedule(self, schedule_group, group: Group):
        for discipline in schedule_group.json()["data"]["rasp"]:
            group.add_schedule(
                datetime.datetime.strptime(discipline["дата"], "%Y-%m-%dT%H:%M:%S"),
                Lesson(
                    discipline["код"],
                    discipline["дисциплина"],
                    discipline["аудитория"],
                    discipline["преподаватель"],
                    discipline["дата"],
                    discipline["начало"],
                    discipline["конец"],
                ),
            )
        stroke = ""
        return self._schedule_to_str(group, "all")

    def _schedule_to_str(self, group: Group, weekday):
        # Получение данных из переменной schedule

        stroke = f"День: {weekday} \n "
        for day, lessons in group.lessons.items():
            if lessons is not None:
                if weekday == "all":
                    for lesson in lessons:
                        stroke += f"\n{lesson.start}:{lesson.end} | {lesson.name}\n{lesson.teacher}\n Аудитория:{lesson.aud}\n\n"
                elif weekday == day:
                    for lesson in lessons:
                        stroke += f"\n{lesson.start}:{lesson.end} | {lesson.name}\n{lesson.teacher}\n Аудитория:{lesson.aud}\n\n"
        return stroke

    # Функция отдает расписание группы по ее наименованию
    def _get_schedule(self, group: Group):
        params = {"idGroup": group.id}

        response = requests.get(Links.schedule_group, params=params)

        if response.status_code == 200:
            return self._collect_schedule(response, group)
        else:
            print("Произошла ошибка при выполнении запроса.")


# # Как дергать методы:
# disp = (
#     Dispatcher_DSTU()
# )  # Создаем класс диспетчера ответственный за отправку запросов и сборку всех данных
# disp.get_groups()  # Получаем все группы. Возвращает список. Обязательно деруть метод один раз, чтобы получить все группы
# # перед тем как получить расписание. Можно по идеи добавить его в метод получения расписания
# print(disp.get_schedule("ИСП9-К22"))  # Получаем группу вместе с ее расписанием
