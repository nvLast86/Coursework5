import psycopg2

class DBEditor:


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
                    vacancy_id INTEGER PRIMARY KEY,
                    employer_id FOREIGN KEY INT REFERENCES employers(employer_id),
                    vacancy_name VARCHAR NOT NULL,
                    publish_date DATE,
                    vacancy_description TEXT,
                    experience VARCHAR,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    area VARCHAR(200),
                    vacancy_link TEXT
                )
            """)
