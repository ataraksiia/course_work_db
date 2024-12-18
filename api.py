import requests


class HH:
    hh_api = "https://api.hh.ru/"

    @staticmethod
    def get_company(employer_id):
        """Функция получает информацию о работодателе."""
        url = f"{HH.hh_api}/employers/{employer_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_vacancies(employer_id):
        """Функция получает информацию о вакансии."""
        url = f"{HH.hh_api}/vacancies"
        params = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
