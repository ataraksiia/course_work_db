import psycopg2

from api import HH
from db_manager import DBManager
from work_with_db import (add_company, add_vacancy, create_database,
                          create_tables)


def main():
    """Функция взаимодействия с пользователем."""
    create_database()
    create_tables()

    conn = psycopg2.connect(
        dbname="vacancies_db",
        user="postgres",
        password="simplepassword123",
        host="localhost",
    )

    employer_ids = [1455, 1740, 78638]

    for employer_id in employer_ids:
        employer_data = HH.get_company(employer_id)
        vacancies = HH.get_vacancies(employer_id)

        company_id = add_company(
            conn,
            employer_data["name"],
            employer_data.get("description", ""),
            employer_data.get("vacancies_url", ""),
        )

        for vacancy in vacancies:
            salary_info = vacancy.get("salary")
            salary = salary_info.get("from") if salary_info else None

            add_vacancy(
                conn, vacancy["name"], salary, vacancy.get("alternate_url"), company_id
            )

    db_manager = DBManager(
        dbname="vacancies_db", user="postgres", password="simplepassword123"
    )

    number = input(
        """Что нужно вывести? (Введите цифру)
    1 - Список количества вакансий компаний.
    2 - Спискок всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки на вакансию.
    3 - Среднюю зарплату по вакансиям.
    4 - Список вакансий с зарплатой выше среднего.
    5 - Поиск по слову.\n"""
    )
    if number == "1":
        print(db_manager.get_companies_and_vacancies_count())
    elif number == "2":
        print(db_manager.get_all_vacancies())
    elif number == "3":
        print(db_manager.get_avg_salary())
    elif number == "4":
        print(db_manager.get_vacancies_with_higher_salary())
    elif number == "5":
        keyword = input("Впишите запрос:\n")
        print(db_manager.get_vacancies_with_keyword(keyword))

    conn.close()


if __name__ == "__main__":
    main()
