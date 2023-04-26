import requests
from datetime import datetime


class HeadHunter:
    """
    Класс HeadHunter создан для работы с сайтом hh.ru. Экземпляры класса создаются на основе переданного
    ключевого слова от пользователя. Далее идет формирование списка вакансий.
    """
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword):
        self.keyword = keyword
        self.vacancies = []
        self.get_vacancies()

    def __repr__(self):
        return f'Результат парсинга по сайту HeadHunter.ru по ключевому слову {self.keyword}\n' \
               f'Количество вакансий: {len(self.vacancies)}'

    def get_vacancies(self):
        """
        Метод получения с сайта hh.ru вакансий на основе ключевого слова пользователя.
        :return: список вакансий по ключевому слову.
        """
        for i in range(5):
            params = {'text': self.keyword, 'employer_id': 3529, 'area': 113, 'page': i, 'per_page': 100}
            response = requests.get(HeadHunter.url, params=params).json()['items']
            self.correct_vacancies(response)
            for vacancy in response:
                self.vacancies.append(Vacancy('HeadHunter',
                                              vacancy['id'],
                                              vacancy['name'],
                                              vacancy['employer']['name'],
                                              vacancy['area']['name'],
                                              [int(vacancy['salary']['from']), int(vacancy['salary']['to']),
                                               vacancy['salary']['currency']],
                                              vacancy['experience'] if 'experience' in vacancy.keys() else 'не указан',
                                              'отсутствует' if vacancy.get('snippet').get('responsibility') is None else
                                              vacancy.get('snippet').get('responsibility'),
                                              vacancy['alternate_url'],
                                              self.format_date(vacancy['published_at'])))
        return self.vacancies

    @staticmethod
    def correct_vacancies(response: dict):
        """
        Статистический метод корректировки полученного ответа от сайта.
        Отсутствующие или равные None значения заменяются на нули или ''
        """
        for item in response:
            if item['salary'] is None:
                item['salary'] = {'from': 0, 'to': 0, 'currency': ''}
            if 'from' not in item['salary'].keys():
                item['salary']['from'] = 0
            if 'to' not in item['salary'].keys():
                item['salary']['to'] = 0
            if item['salary']['from'] is None:
                item['salary']['from'] = 0
            if item['salary']['to'] is None:
                item['salary']['to'] = 0

    @staticmethod
    def format_date(value):
        """
        Статистический метод вывода времени публикации вакансии в формате,
        удобный для пользователя
        """
        date = datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M:%S")
        return date
