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


if __name__ == '__main__':
    test = DBCreator('test1', config())
    test.create_database()
    test.create_tables()
