import psycopg2
from src.parser import HeadHunterAPIVacancies as HH


def create_and_fill_tables():
    conn_params = {'host': 'localhost', 'database': 'course_project 5', 'user': 'postgres', 'password': '5621'}

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
    #
            hh = HH()
            vacancies_hh = hh.get_vacancies('python')

            cur.execute('''CREATE TABLE employers(
    employer_id VARCHAR(50) PRIMARY KEY,
    employer_name VARCHAR(255),
    employer_url VARCHAR(255),
    employer_alternate_url VARCHAR(255))''')
            cur.execute('''CREATE TABLE vacancies(
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    url VARCHAR(255),
    alternate_url VARCHAR(255),
    experience VARCHAR(50),
    city VARCHAR(50),
    employer_id VARCHAR(50),
    FOREIGN KEY (employer_id) REFERENCES employers(employer_id))''')
            cur.execute('''CREATE TABLE salaries(
    salary_id SERIAL PRIMARY KEY,
    salary_from INT,
    salary_to INT,
    currency VARCHAR(5),
    vacancy_id VARCHAR(50),
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(id))''')

            for vacancy in vacancies_hh:
                if vacancy['salary']:
                    vacancy_id = vacancy['id']
                    vacancy_name = vacancy['name']
                    vacancy_url = vacancy['url']
                    vacancy_alternate_url = vacancy['alternate_url']
                    experience = vacancy['experience']['name']
                    city = vacancy['area']['name']

                    try:
                        employer_id = vacancy['employer']['id']
                    except KeyError:
                        continue
                    employer_name = vacancy['employer']['name']
                    employer_url = vacancy['employer']['url']
                    employer_alternate_url = vacancy['employer']['alternate_url']

                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']
                    currency = vacancy['salary']['currency']

                    cur.execute('SELECT employer_id FROM employers')

                    rows = [el[0] for el in cur.fetchall()]
                    if employer_id not in rows:

                        cur.execute(f'INSERT INTO employers VALUES (%s, %s, %s, %s)',
                                    (employer_id, employer_name, employer_url, employer_alternate_url))
                    cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)',
                                (vacancy_id, vacancy_name, vacancy_url, vacancy_alternate_url, experience, city,
                                 employer_id))
                    cur.execute(f'INSERT INTO salaries (salary_from, salary_to, currency, vacancy_id) '
                                f'VALUES (%s, %s, %s, %s)',
                                (salary_from, salary_to, currency, vacancy_id))


def drop_tables():
    conn_params = {'host': 'localhost', 'database': 'course_project 5', 'user': 'postgres', 'password': '5621'}

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:

            cur.execute("DROP TABLE salaries;")
            cur.execute("DROP TABLE vacancies;")
            cur.execute("DROP TABLE employers;")


# if __name__ == '__main__':
#     create_and_fill_tables()
#     #drop_tables()


