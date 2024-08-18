import psycopg2


class DBManager:
    def __init__(self, database_name, params):
        self.dbname = database_name
        self.conn = psycopg2.connect(dbname=database_name, **params)  # Подключение с использованием database_name
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        self.cur.execute("""
        SELECT COMPANY_NAME, 
        COUNT(*) FROM vacancies
        GROUP BY COMPANY_NAME
        """)
        rows = self.cur.fetchall()
        return {row[0]: row[1] for row in rows}

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        self.cur.execute("""
        SELECT company_name, job_title, salary_from, currency, link_to_vacancy FROM vacancies
        """)
        rows = self.cur.fetchall()
        return rows

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        """
        self.cur.execute("""
        SELECT AVG(salary_from) FROM vacancies""")
        rows = self.cur.fetchall()
        return rows[0][0] if rows else None  # Возвращаем число

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        self.cur.execute("""
        SELECT job_title, salary_from FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
        ORDER BY salary_from DESC
        """)
        rows = self.cur.fetchall()
        return rows

    def get_vacancies_with_keyword(self, keyword) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        q = """SELECT * FROM vacancies
                WHERE LOWER(job_title) LIKE %s"""
        self.cur.execute(q, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()

    def get_company_name(self, company_id) -> str:
        """
        Получает название компании по ее ID
        """
        self.cur.execute(
            """SELECT company_name FROM companies WHERE company_id = %s""", (company_id,)
        )
        result = self.cur.fetchone()
        return result[0] if result else None

    def close_connection(self):
        """
        Закрывает подключение к БД.
        """
        self.cur.close()
        self.conn.close()


