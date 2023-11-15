import requests
from api.url import Links
from api.group import Group
from api.schedule import Lesson
import datetime


class Dispatcher_DSTU:
    _groups = []
    _schedule = []

    # Функция собирает группы
    def _collect_groups(self, raspGroupList: dict):
        for item in raspGroupList["data"]:
            if item["facul"] == "АТК":
                self._groups.append(Group(item["id"], item["name"]))

    # Функция для получения групп
    def get_groups(self):
        params = {"year": "2023-2024"}

        response = requests.get(Links.rasp_group_list, params=params)

        if response.status_code == 200:
            self._collect_groups(response.json())
            return [group.name for group in self._groups]
        else:
            print("Произошла ошибка при выполнении запроса.")

    # Функция находит группу по ее наименованию
    def _find_group(self, group_name: str):
        for group in self._groups:
            if group.name == group_name:
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
        return group
        # group.schedule.append(
        #     Schedule(
        #         discipline["код"],
        #         discipline["дисциплина"],
        #         discipline["аудитория"],
        #         discipline["преподаватель"],
        #         discipline["дата"],
        #         discipline["начало"],
        #         discipline["конец"],
        #     )
        # )

    # Функция отдает расписание группы по ее наименованию
    def get_schedule(self, group_name: str):
        group = self._find_group(group_name)

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
