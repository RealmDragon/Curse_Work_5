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
    print(f"Выберите запрос: "
          f"1 - Список всех компаний и количество вакансий у каждой компании"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"
          f"3 - Средняя зарплата по вакансиям"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово")
    user_answer = input("Введите номер запроса")
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
