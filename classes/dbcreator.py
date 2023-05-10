import psycopg2
import psycopg2
from utils.config import config
from headhunter import HeadHunter


class DBCreator:

    def __init__(self, db_name, params):
        self.db_name = db_name
        self.params = params

    def create_database(self):
        """Создает базу данных и таблицы"""
        # Подключаемся к postgres, чтобы создать БД
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cur.execute(f"CREATE DATABASE {self.db_name}")

        except:
            # Если было активное подключение, удаляет его, удаляет БД и создает ее заново
            cur.execute("SELECT pg_terminate_backend(pg_stat_activity.pid) "
                        "FROM pg_stat_activity "
                        f"WHERE pg_stat_activity.datname = '{self.db_name}' ")
            cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cur.execute(f"CREATE DATABASE {self.db_name}")

        finally:
            cur.close()
            conn.close()

    def create_tables(self):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""CREATE TABLE IF NOT EXISTS employers (
                                       employer_id INTEGER PRIMARY KEY,
                                       employer_name VARCHAR(200) NOT NULL)""")

                    cur.execute("""CREATE TABLE IF NOT EXISTS vacancies (
                                       vacancy_id INTEGER PRIMARY KEY,
                                       employer_id INTEGER  REFERENCES employers(employer_id) NOT NULL,
                                       vacancy_name VARCHAR(300) NOT NULL,
                                       description TEXT,
                                       experience VARCHAR(100),
                                       salary_from INTEGER,
                                       salary_to INTEGER,
                                       area VARCHAR(200),
                                       link TEXT,
                                       publish_date DATE)""")
        finally:
            conn.close()

    def insert_data(self, data, is_employers=True):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    for employer_data in data:
                        if is_employers:
                            cur.execute("""INSERT INTO employers (employer_id, employer_name) 
                                           VALUES (%s, %s)""", (employer_data['id'], employer_data['name']))
                        else:
                            cur.execute("""INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, 
                                           description, experience, salary_from, salary_to, area, link, 
                                           publish_date)
                                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                           (employer_data['vacancy_id'], employer_data['employer_id'],
                                            employer_data['vacancy_name'], employer_data['description'],
                                            employer_data['experience'], employer_data['salary_from'],
                                            employer_data['salary_to'], employer_data['area'],
                                            employer_data['link'], employer_data['publish_date']))
        finally:
            conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Функция для получения списка всех компаний и количества вакансий у каждой компании
        """
        sql_request = """SELECT employer_name, COUNT(vacancies.vacancy_id) FROM employers
                         JOIN vacancies USING (employer_id)
                         GROUP BY employer_name"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql_request)
                    result = cur.fetchall()
        finally:
            conn.close()
            return result

    def get_all_vacancies(self):
        """
        Функция получения списка всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию
        """
        sql_request = """SELECT vacancy_name, employers.employer_name, salary_from, salary_to,
                         vacancy_link FROM vacancies
                         JOIN employers USING (employer_id)"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql_request)
                    result = cur.fetchall()
                    # return result
        finally:
            conn.close()
            return result

    def get_avg_salary(self):
        """
        Функция получения средней зарплаты по вакансиям
        """
        sql_request = """SELECT employers.employer_name, ROUND(AVG (salary_from)) as avg_salary_from,
                         ROUND(AVG(salary_to)) as avg_salary_to FROM vacancies
                         JOIN employers USING (employer_id)
                         GROUP BY employers.employer_name"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql_request)
                    result = cur.fetchall()
                    # return result
        finally:
            conn.close()
            return result

    def get_vacancies_with_higher_salary(self):
        """
        Функция получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        sql_request = """SELECT vacancy_name, salary_from FROM vacancies
                         WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql_request)
                    result = cur.fetchall()
                    # return result
        finally:
            conn.close()
            return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Функция получения списка всех вакансий, в названии которых содержатся
        переданные в метод слова, например “python”
        """
        sql_request = f"SELECT vacancy_name, employers.employer_name FROM vacancies " \
                      f"JOIN employers USING (employer_id) " \
                      f"WHERE vacancy_name LIKE '%{keyword}%'"
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql_request)
                    result = cur.fetchall()
                    # return result
        finally:
            conn.close()
            return result


if __name__ == '__main__':
    hh = HeadHunter()
    test = DBCreator('test', config())
    test.create_database()
    test.create_tables()
    test.insert_data(hh.employers)
    test.insert_data(hh.vacancies, False)
    test.get_companies_and_vacancies_count()
    # print(something)

