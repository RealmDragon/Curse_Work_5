import requests

def get_companies() -> list:
    """
    Получение названия компаний и их ID
    """
    companies_data = {
        'Тиньков': 78638,
        'Яндекс': 1740,
        'Лаборатория Касперского': 1057,
        'Сбербанк': 1473866,
        'Банк ВТБ': 4181,
        'Газпромнефть': 39305,
        'Альфа-банк': 80,
        'VK': 15478,
        'ПАО Ростелеком': 2748,
        'Циан': 1429999
    }

    data = []

    for company_name, company_id in companies_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        company_info = {'company_id': company_id, "company_name": company_name, "company_url": company_url}
        data.append(company_info)

    return data


def get_vacancies(data: list) -> list[dict]:
    """
    Получение информации о компаниях
    """
    vacancies = []
    for company in data:
        company_id = company["company_id"]
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancy = response.json()['items']
            vacancies.extend(vacancy)
        else:
            print(f"Ошибка при запросе компании {company['company_name']}: {response.status_code}")
    return vacancies


def get_vacancy_list(data: list) -> list[dict]:
    """
    Преобразование информации о компаниях для дальнейшей работы с БД
    """
    vacancy_list = []
    for item in data:
        company_name = item["employer"]["name"]
        company_id = item["employer"]["id"]
        company_url = item["employer"]["url"]
        job_title = item["name"]
        link_to_vacancy = item["employer"]["alternate_url"]
        salary = item["salary"]
        salary_from = 0
        currency = " "
        description = item["snippet"]["responsibility"]
        experience = item["experience"]["name"]
        requirement = item['snippet']['requirement']
        if salary:
            salary_from = item["salary"]["from"]
            if not salary_from:
                salary_from = 0
            currency = item["salary"]["currency"]
            if not currency:
                currency = " "
        if not experience:
            experience = "Информация отсутсвует"

        vacancy_list.append(
            {
                "company_id": company_id,
                "company_name": company_name,
                "company_url": company_url,
                "job_title": job_title,
                "link_to_vacancy": link_to_vacancy,
                "salary_from": salary_from,
                "salary_to": salary,
                "currency": currency,
                "experience": experience,
                "description": description,
                "requirement": requirement


            }
        )
    return vacancy_list



import psycopg2

from src.config import config  # Импортируем config из этой директории
from src.create_db import create_database, save_data_to_db  # Импортируем create_data_base и save_data_to_db
from src.db_manager import DBManager  # Импортируем DBManager
from src.hh_api import get_vacancies, get_companies, get_vacancy_list  # Импортируем функции из hh_api

params = config()  # Получаем параметры подключения к БД
data = get_vacancies(get_companies())  # Получаем список вакансий
vacancies = get_vacancy_list(data)  # Преобразуем список вакансий в нужный формат

create_database("top_vacancies", params)  # Создаем базу данных "top_vacancies"
conn = psycopg2.connect(dbname="top_vacancies", **params)  # Подключаемся к базе данных
save_data_to_db(vacancies, "top_vacancies", params)  # Сохраняем данные в базу данных

def interfaсe():
    """
    Функция для взаимодействия с пользователем
    """
    db_manager = DBManager("top_vacancies", params)  # Создаем объект DBManager
    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n")
    user_answer = input("Введите номер запроса\n")
    if user_answer == "1":
        companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
        print(f"Список всех компаний и количество вакансий у каждой компании: {companies_and_vacancies_count}")
    elif user_answer == "2":
        all_vacancies = db_manager.get_all_vacancies()
        print(f"Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию: {all_vacancies}")
    elif user_answer == "3":
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата по вакансиям: {avg_salary}")
    elif user_answer == "4":
        vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
        print(f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: {vacancies_with_higher_salary}")
    elif user_answer == "5":
        user_input = input(f'Введите слово: ')
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
        print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово: {vacancies_with_keyword}")
    else:
        print("Введен неверный запрос")

interfaсe()
import requests
import psycopg2
from typing import Any

employer_ids = [9694561, 4219, 5919632, 5667343, 9301808, 774144, 10571093, 198614, 6062708, 4306]


def get_employee_data():
    """
    функция для получения данных о компаниях с сайта HH.ru
    :return: список компаний
    """
    employers = []
    for employer_id in employer_ids:
        url_emp = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(url_emp, ).json()
        employers.append(employer_info)

    return employers


def get_vacancies_data():
    """
    функция для получения данных о вакансиях с сайта HH.ru
    :return: список вакансий
    """
    vacancy = []
    for vacacies_id in employer_ids:
        url_vac = f"https://api.hh.ru/vacancies?employer_id={vacacies_id}"
        vacancy_info = requests.get(url_vac, params={'page': 0, 'per_page': 100}).json()
        vacancy.extend(vacancy_info['items'])
    return vacancy


def create_database(database_name: str, params: dict) -> None:
    """
    функция для создания Базы Данных и создания таблиц в БД
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER,
                employer_name text not null,
                employer_area TEXT not null,
                url TEXT,
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancy (
                vacancy_id INTEGER,
                vacancy_name VARCHAR,
                vacancy_area VARCHAR,
                salary INTEGER,
                employer_id INTEGER,
                vacancy_url VARCHAR
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database_emp(data_emp: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция для заполнения таблицы компаний в БД
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in data_emp:
            cur.execute("""
                INSERT INTO employers (employer_id, employer_name, employer_area, url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                """,
                        (emp['id'], emp['name'], emp['area']['name'], emp['alternate_url'], emp['open_vacancies']))

    conn.commit()
    conn.close()


def save_data_to_database_vac(data_vac: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция для заполнения таблицы вакансий в БД
    """

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vac in data_vac:
            if vac['salary'] is None or vac['salary']['from'] is None:
                cur.execute("""
                   INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """,
                            (vac.get('id'), vac['name'], vac['area']['name'], 0, vac['employer']['id'],
                             vac['alternate_url']))
            else:
                cur.execute("""
                    INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                            (vac.get('id'), vac['name'], vac['area']['name'], vac['salary']['from'],
                             vac['employer']['id'], vac['alternate_url']))

    conn.commit()
    conn.close()



