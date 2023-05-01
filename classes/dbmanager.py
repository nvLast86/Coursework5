import psycopg2


class DBManager(DBEditor):


    def get_companies_and_vacancies_count(self):
        """
        Функция для получения списка всех компаний и количества вакансий у каждой компании
        """
        sql_request = """SELECT employer_name, COUNT(vacancies.vacancy_id) FROM employers
                         INNER JOIN vacancies USING (employer_id)
                         GROUP BY employer_name"""

    def get_all_vacancies(self):
        """
        Функция получения списка всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию
        """
        sql_request = """SELECT vacancy_name, employers.employer_name, salary_from, salary_to, 
                         vacancy_link FROM vacancies
                         INNER JOIN employers USING (employer_id)"""

    def get_avg_salary(self):
        """
        Функция получения средней зарплаты по вакансиям
        """
        sql_request = """SELECT employers.employer_name, ROUND(AVG (salary_from)) as avg_salary_from, 
                         ROUND(AVG(salary_to)) as avg_salary_to FROM vacancies
                         INNER JOIN employers USING (employer_id)
                         GROUP BY employers.employer_name"""
    def get_vacancies_with_higher_salary(self):
        """
        Функция получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        sql_request = """SELECT vacancy_name, salary_from FROM vacancies
                         WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)"""

    def get_vacancies_with_keyword(self):
        """
        Функция получения списка всех вакансий, в названии которых содержатся
        переданные в метод слова, например “python”
        """
        sql_request = """SELECT vacancy_name, employers.employer_name FROM vacancies
                         INNER JOIN employers USING (employer_id)
                         WHERE vacancy_name LIKE '%python%'"""



