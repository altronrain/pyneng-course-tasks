# -*- coding: utf-8 -*-
"""
Задание 6.5

Функция randint(1, 9) при каждом вызове возвращает случайное число из диапазона
от 1 до 9 (включая 1 и 9). Попробуйте запустить код задания несколько раз,
значение random_number будет меняться.

В этом задании пишем игру по угадыванию числа.
С помощью randint получаем случайное число random_number от 1 до 9 (эта часть сделана).
Затем надо дать пользователю 5 попыток на то чтобы угадать это значение.

На каждой попытке надо запросить у пользователя ввод числа в диапазоне от 1 до 9.
Если введенное пользователем значение равно random_number, вывести на экран
сообщение "Правильно!" и остановить игру.

Если введенное пользователем значение не равно random_number:
* если random_number больше введенного значения, вывести на экран сообщение "Задуманное число больше"
* если random_number меньше введенного значения, вывести на экран сообщение "Задуманное число меньше"

Если после 5ти попыток число не угадано, вывести "Число не угадано после 5 попыток".

Пример выполнения задания для числа 3
$ python task_6_5.py
Введите число: 1
Задуманное число больше
Введите число: 6
Задуманное число меньше
Введите число: 2
Задуманное число больше
Введите число: 5
Задуманное число меньше
Введите число: 4
Задуманное число меньше
Число не угадано после 5 попыток

Пример выполнения задания для числа 7
$ python task_6_5.py
Введите число: 6
Задуманное число больше
Введите число: 9
Задуманное число меньше
Введите число: 8
Задуманное число меньше
Введите число: 7
Правильно!

"""
from random import randint

random_number = randint(1, 9)
# print(random_number)

for attempt in range(0, 5):
    user_number = input("Введите число: ")
#    if user_num.isdigit() and int(user_number) in range(1,10):  
    if int(user_number) > random_number:
        print("Задуманное число меньше")
        attempt += 1
    elif int(user_number) < random_number:
        print("Задуманное число больше")
        attempt += 1
    else:
        print("Правильно!")
        break
#    else:
#        print("Необходимо ввести число в диапазоне от 1 до 9")        
    
else:
    print("Число не угадано после 5 попыток")