from classes.headhunter import HeadHunter
from classes.dbmanager import DBManager
from utils.config import config


def main():
    # Создаем БД и выгружаем данные с сайта hh.ru
    print("Добро пожаловать!")
    print("Идет сборка данных, пожалуйста, подождите...")
    print("Может занять длительное время!\n")
    hh = HeadHunter()
    params = config()
    db = DBManager('headhunter', params)
    db.create_database()
    db.create_tables()
    db.insert_data(hh.employers)
    db.insert_data(hh.vacancies, False)

    # Предлагаем пользователю поработать с БД
    print(db)
    print(f'На данный момент в базе данных {len(hh.vacancies)} вакансий.\n')
    while True:
        user_answer = input('Пожалуйста, введите номер действия (или "x" для выхода):\n')
        if user_answer == '1':
            print(db.get_companies_and_vacancies_count())
        elif user_answer == '2':
            print(db.get_all_vacancies())
        elif user_answer == '3':
            print(db.get_avg_salary())
        elif user_answer == '4':
            print(db.get_vacancies_with_higher_salary())
        elif user_answer == '5':
            user_keyword = input('Пожалуйста, введите ключевое слово:\n')
            print(db.get_vacancies_with_keyword(user_keyword))
        elif user_answer in ['x', 'X']:
            break
        else:
            print("Неправильный ввод! Повторите пожалуйста")

    print('Спасибо за работу!')


if __name__ == '__main__':
    main()

