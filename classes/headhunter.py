import requests
from datetime import datetime
import json


class HeadHunter:
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

    def get_vacancies(self):
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



if __name__ == '__main__':
    test = HeadHunter()
    x = json.dumps(test.vacancies, ensure_ascii=False)
    with open('test.txt', 'w', encoding='utf-8') as outfile:
        json.dump(x, outfile, ensure_ascii=False)

















