from src.config import config
from src.create_db import create_database, save_data_to_db
from src.db_manager import DBManager
from src.hh_api import get_vacancies, get_companies, get_vacancy_list



def main():
    # Получаем данные из API HH.ru
    company_ids = [
        '4307',
        '4787018',
        '4219',
        '5557093',
        '1579449',
        '2180',
        '1057',
        '1180',
        '208707',
        '205'
    ]
    params = config()
    companies_data = get_companies()
    vacancies_data = get_vacancies(companies_data)
    vacancies = get_vacancy_list(vacancies_data)

    # Создаем базу данных и заполняем ее данными
    create_database('hh', params)
    save_data_to_db(companies_data, vacancies, 'hh', params)

    # Создаем объект DBManager для работы с базой данных
    db_manager = DBManager("hh", params)

    # Выводим меню
    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n"
          f"6 - Получить название компании по ее ID\n")
    user_answer = input("Введите номер запроса\n")

    # Обрабатываем запросы
    if user_answer == "1":
        companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
        print(f"Список всех компаний и количество вакансий у каждой компании: {companies_and_vacancies_count}\n")
    elif user_answer == "2":
        all_vacancies = db_manager.get_all_vacancies()
        print(
            f"Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию: {all_vacancies}\n")
    elif user_answer == "3":
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата по вакансиям: {avg_salary}\n")
    elif user_answer == "4":
        vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
        print(
            f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: {vacancies_with_higher_salary}\n")
    elif user_answer == "5":
        user_input = input(f'Введите слово: ')
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
        print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово: {vacancies_with_keyword}")
    elif user_answer == "6":
        company_id = input(f'Введите ID компании: ')
        company_name = db_manager.get_company_name(company_id)  # Эта функция не определена
        print(f"Название компании: {company_name}")
    else:
        print("Введен неверный запрос")


if __name__ == '__main__':
    main()





