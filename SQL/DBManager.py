import psycopg2
import json


class DBManager:

    def __init__(self, host, db_name, user_name, password):
        self.host = host
        self.db_name = db_name
        self.user_name = user_name
        self.password = password
        self.conn = None

    def __connect(self):
        """Подключение к БД"""
        try:
            self.conn = psycopg2.connect(host=self.host, database=self.db_name, user=self.user_name, password=self.password)
            print('Успешное подключение к БД')
        except psycopg2.Error as e:
            print(f'Ошибка при подключении к БД: {e}')

    def __close_connection(self):
        ''' Закрываем подключение к бд '''
        if self.conn:
            self.conn.close()
            print('Подключение к базе данных закрыто')

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """
        self.__connect()
        if not self.conn:
            print('Нет подключения к бд')
            return None

        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT employer_name, COUNT(*) AS count_vacancies FROM employers "
                        f"JOIN vacancies ON employers.employer_id=vacancies.employer_id "
                        f"GROUP BY employer_name;")
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}')
        finally:
            self.__close_connection()

    def get_all_vacancies_with_some_columns(self):
        """ Получает список всех вакансий
        с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию """
        self.__connect()
        if not self.conn:
            print('Нет подключения к бд')
            return None

        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT employers.employer_name, vacancies.name, salaries.salary_from, salaries.salary_to, salaries.currency, vacancies.url "
                        f"FROM employers "
                        f"JOIN vacancies ON employers.employer_id=vacancies.employer_id "
                        f"JOIN salaries ON salaries.vacancy_id=vacancies.id;")
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}')
        finally:
            self.__close_connection()

    def get_all_vacancies(self):
        """ Получает список всех вакансий со всеми колонками """
        self.__connect()
        if not self.conn:
            print('Нет подключения к бд')
            return None

        cur = self.conn.cursor()
        try:
            cur.execute(
                f"SELECT * "
                f"FROM employers "
                f"JOIN vacancies ON employers.employer_id=vacancies.employer_id "
                f"JOIN salaries ON salaries.vacancy_id=vacancies.id;")
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}')
        finally:
            self.__close_connection()

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям """
        self.__connect()
        if not self.conn:
            print('Нет подключения к бд')
            return None

        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT AVG(salary_from) AS avg_salary FROM salaries;")
            result = round(cur.fetchall()[0][0])
            return result
        except psycopg2.Error as e:
            print(f"Произошла ошибка: {e}")
        finally:
            self.__close_connection()

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        self.__connect()
        if not self.conn:
            print('Нет подключения к бд')
            return None

        cur = self.conn.cursor()
        avg_salary = self.get_avg_salary()
        try:
            cur.execute(f"SELECT * "
                        f"FROM vacancies "
                        f"JOIN salaries ON vacancies.id=salaries.vacancy_id "
                        f"WHERE salaries.salary_from > {avg_salary};")
            result = cur.fetchall()
            vacancies_with_higher_salary = []
            for vacancy in result:
                vacancies_with_higher_salary.append(vacancy)
            return vacancies_with_higher_salary
        except psycopg2.Error as e:
            print(f"Произошла ошибка: {e}")
        finally:
            self.__close_connection()

    def get_vacancies_with_keyword(self, keyword):
        """ Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python """
        self.__connect()
        if not self.conn:
            print('Нет подключения к бд')
            return None

        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT * "
                        f"FROM vacancies "
                        f"JOIN salaries ON vacancies.id=salaries.vacancy_id "
                        f"WHERE lower(name) LIKE '%{keyword.lower()}%';")
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            print(f"Произошла ошибка: {e}")
        finally:
            self.__close_connection()