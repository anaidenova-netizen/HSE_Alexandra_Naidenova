"""
Задание 1.
Работа с переменными, вводом и выводом данных.
"""

name = "Alexandra"
age = 18
city = "Moscow"

print("Имя:", name)
print("Возраст:", age)
print("Город:", city)

user_name = input("Введите ваше имя: ")
user_number = input("Введите любое число: ")

print("Вы ввели имя:", user_name)
print("Вы ввели число:", user_number)

a = 10
print("Значение a:", a)
print("id(a) до изменения:", id(a))

a = 20
print("Новое значение a:", a)
print("id(a) после изменения:", id(a))


"""
Задание 2.
Пользователь вводит время в секундах.
Нужно перевести его в часы, минуты и секунды.
"""

seconds_input = input("Введите время в секундах: ")

if seconds_input.isdigit():
    total_seconds = int(seconds_input)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    print("Часы:", hours)
    print("Минуты:", minutes)
    print("Секунды:", seconds)
else:
    print("Ошибка: нужно ввести только число.")


"""
Задание 3.
Пользователь вводит число n от 1 до 9.
Нужно найти сумму n + nn + nnn.
"""

n = input("Введите число от 1 до 9: ")

if n.isdigit() and 1 <= int(n) <= 9:
    result = int(n) + int(n * 2) + int(n * 3)
    print("Сумма n + nn + nnn =", result)
else:
    print("Ошибка: введите число от 1 до 9.")
