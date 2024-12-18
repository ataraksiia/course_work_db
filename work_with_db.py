import psycopg2


def create_database():
    """Функция создает базу данных."""
    conn = psycopg2.connect(
        dbname="postgres", user="postgres", password="moon", host="localhost"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS vacancies_db;")
    cursor.execute("CREATE DATABASE vacancies_db;")
    cursor.close()
    conn.close()


def create_tables():
    """Функция создает таблицы."""
    conn = psycopg2.connect(
        dbname="vacancies_db", user="postgres", password="moon", host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        vacancies_url VARCHAR(255)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        salary INTEGER,
        url VARCHAR(255),
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE
    );
    """
    )

    conn.commit()
    cursor.close()
    conn.close()


def add_company(conn, name, description, vacancies_url):
    """Функция создает компанию."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO companies (name, description, vacancies_url)
        VALUES (%s, %s, %s) RETURNING id;
    """,
        (name, description, vacancies_url),
    )
    company_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return company_id


def add_vacancy(conn, title, salary, url, company_id):
    """Функция создает вакансию."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO vacancies (title, salary, url, company_id)
        VALUES (%s, %s, %s, %s)
    """,
        (title, salary, url, company_id),
    )
    conn.commit()
    cursor.close()
