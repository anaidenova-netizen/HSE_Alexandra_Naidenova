"""
Задание 1.
Создание функций для математических вычислений:
1. Факториал числа
2. Наибольшее число из трех
3. Площадь прямоугольного треугольника
"""

from lesson_2_data import respondents, courts


def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def max_of_three(numbers):
    return max(numbers)


def triangle_area(a, b):
    return (a * b) / 2


print("Факториал числа 5:", factorial(5))
print("Наибольшее число из (3, 7, 5):", max_of_three((3, 7, 5)))
print("Площадь прямоугольного треугольника:", triangle_area(6, 8))


"""
Задание 2.
Создание функции для генерации шапки процессуального документа.
"""


def find_court(case_number):
    court_code = case_number.split("-")[0]

    for court in courts:
        if court["court_code"] == court_code:
            return court

    return None


def make_header(respondent, case_number):
    court = find_court(case_number)

    if court is None:
        return f"Суд для дела {case_number} не найден."

    text = f"""В {court["court_name"]}
Адрес: {court["court_address"]}

Истец: Наиденова Александра
ИНН 123456789012 ОГРНИП 123456789012345
Адрес: 123456, г. Москва, ул. Примерная, д. 1

Ответчик: {respondent["short_name"]}
ИНН {respondent["inn"]} ОГРН {respondent["ogrn"]}
Адрес: {respondent["address"]}

Номер дела {case_number}"""

    return text


def print_headers(respondents_list):
    for respondent in respondents_list:
        if "case_number" in respondent:
            print(make_header(respondent, respondent["case_number"]))
            print("-" * 80)


print_headers(respondents[:5])
