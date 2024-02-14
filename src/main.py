from src.classes import HH_API, Vacancy, JsonSaver


def user_interaction():
    hh_api = HH_API('https://api.hh.ru/vacancies')
    vacancy_storage = JsonSaver('vacancies.json')
    user_vacancy = input('Введите вакансию ')
    hh_vacancies = hh_api.get_vacancies(user_vacancy)

    for vacancy in hh_vacancies:
        if vacancy['salary']['currency'] != 'RUR':
            hh_vacancies.remove(vacancy)

    hh_vacancies = [Vacancy.instant_from_lst(vacancy) for vacancy in hh_vacancies]

    print('Хотите отфильтровать вакансии по ключевому слову в описании? (yes/no)')
    user_input = input()
    if user_input == 'yes':
        keyword = input('Введите ключевое слово: ')
        for vacancy in hh_vacancies:
            if keyword.lower() not in vacancy.description.lower():
                hh_vacancies.remove(vacancy)

    sorted_vacancies = sorted(hh_vacancies, reverse=True)
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    vacancy_list = []
    for i in range(top_n):
        print(sorted_vacancies[i])
        vacancy_list.append(sorted_vacancies[i].__dict__)

    vacancy_storage.add_vacancies(vacancy_list)

    print('Хотите очистить файл? (yes/no)')
    user_input = input()
    if user_input == 'yes':
        vacancy_storage.del_vacancies()
        print('Программа завершена, файл очищен')
    else:
        print('Программа завершена, файл сохрвнён')


if __name__ == "__main__":
    user_interaction()
