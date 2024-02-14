from abc import ABC, abstractmethod
import requests
import json


class API(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class HH_API(API):

    def __init__(self, url):
        super().__init__(url)

    def get_vacancies(self, keyword):
        params = {
            'text': keyword,
            'per_page': 100,
            'only_with_salary': True,
            'currency': 'RUR',
        }

        response = requests.get(self.url, params=params)
        vacancies = response.json()['items']
        return vacancies


class Vacancy:

    def __init__(self, name, description, salary_from, salary_to, currency, url):
        self.name = name
        self.description = description if description else ''
        self.salary_from = salary_from if salary_from else 0
        self.salary_to = salary_to if salary_to else salary_from
        self.currency = currency
        self.url = url

    def __str__(self):
        return f"{self.name}, Зарплата: {self.salary_to} {self.currency}, Описание: {self.description} {self.url}"

    def __lt__(self, other):
        return self.salary_to < other.salary_to

    @classmethod
    def instant_from_lst(cls, vacancy):
        return cls(vacancy['name'], vacancy['snippet']['requirement'], vacancy['salary']['from'],
                   vacancy['salary']['to'], vacancy['salary']['currency'], vacancy['alternate_url'])


class BasicSaver(ABC):
    def __init__(self, filename):
        self.filename = filename

    def add_vacancies(self, list_of_vacancies):
        pass

    def del_vacancies(self):
        pass


class JsonSaver(BasicSaver):
    def __init__(self, filename):
        super().__init__(filename)

    def add_vacancies(self, list_of_vacancies):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(list_of_vacancies, file, indent=4)
            file.write('\n')

    def del_vacancies(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write('')

