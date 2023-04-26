import psycopg2


class DBManager:

    def create_database(database_name: str, params: dict) -> None:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE employers (
                        employer_id INTEGER PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        description TEXT
                    )
                """)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        channel_id INT REFERENCES channels(channel_id),
                        title VARCHAR NOT NULL,
                        publish_date DATE,
                        video_url TEXT
                    )
                """)

    def get_companies_and_vacancies_count(self):
        """
        Функция для получения списка всех компаний и количества вакансий у каждой компании
        """

    def get_all_vacancies(self):
        """
        Функция получения списка всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию
        """

    def get_avg_salary(self):
        """
        Функция получения средней зарплаты по вакансиям
        """

    def get_vacancies_with_higher_salary(self):
        """
        Функция получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """

    def get_vacancies_with_keyword(self):
        """
        Функция получения списка всех вакансий, в названии которых содержатся
        переданные в метод слова, например “python”
        """




