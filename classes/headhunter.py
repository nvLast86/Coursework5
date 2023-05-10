import requests
from datetime import datetime


class HeadHunter:
    """
    Класс HeadHunter для работы с сайтом hh.ru.
    Создаваемые экземпляры класса содержат список словарей с данными о вакансиях.
    Извлекаются данные о максимум 2000 вакансий (может быть меньше, т.к. не извлекаются вакансии,
    не содержащие никаких данных о зарплате).
    Аттрибуты класса:
    url - базовый URL для работы с API
    employers - список словарей с id и названием 10 компаний
    """
    url = 'https://api.hh.ru/vacancies'
    employers = [{'id': 1740, 'name': 'Яндекс'},
                 {'id': 2180, 'name': 'OZON'},
                 {'id': 3529, 'name': 'СБЕР'},
                 {'id': 8550, 'name': 'Центр финансовых технологий'},
                 {'id': 39305, 'name': 'Газпромнефть'},
                 {'id': 41862, 'name': 'Контур'},
                 {'id': 64174, 'name': '2GIS'},
                 {'id': 67611, 'name': 'Тензор'},
                 {'id': 966315, 'name': 'АО Омский НИИ приборостроения'},
                 {'id': 2326492, 'name': 'Телеком-инжиниринг'}]

    def __init__(self):
        self.vacancies = []
        self.get_vacancies()

    def get_vacancies(self) -> None:
        """
        Метод для получения данных о вакансиях
        """
        for employer in HeadHunter.employers:
            for i in range(20):
                params = {'employer_id': employer['id'], 'area': 113, 'page': i, 'per_page': 100}
                employer_vacancies = requests.get(HeadHunter.url, params=params).json()['items']
                for employer_vacancy in employer_vacancies:
                    if employer_vacancy['salary'] is not None:
                        vacancy = {}
                        vacancy['vacancy_id'] = employer_vacancy['id']
                        vacancy['employer_id'] = employer['id']
                        vacancy['vacancy_name'] = employer_vacancy['name']
                        vacancy['description'] = employer_vacancy['snippet']['responsibility']
                        vacancy['experience'] = employer_vacancy['experience']['name']
                        vacancy['salary_from'] = employer_vacancy['salary']['from']
                        vacancy['salary_to'] = employer_vacancy['salary']['to']
                        vacancy['area'] = employer_vacancy['area']['name']
                        vacancy['link'] = employer_vacancy['alternate_url']
                        vacancy['publish_date'] = datetime.fromisoformat(employer_vacancy['published_at']).\
                            strftime("%Y-%m-%d")
                        self.vacancies.append(vacancy)

