# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.
В файле output первой строкой должны быть заголовки столбцов,
такие же как в файле source_log.

Для части пользователей запись только одна и тогда в итоговый файл надо записать
только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_str_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.
Вторая функция convert_datetime_to_str делает обратную операцию - превращает
объект datetime в строку.

Функции convert_str_to_datetime и convert_datetime_to_str использовать не обязательно.

"""
import os
import csv
import datetime
from pprint import pprint

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/17_serialization"


def convert_str_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")


def convert_datetime_to_str(datetime_obj):
    """
    Конвертирует объект datetime в строку с датой в формате 11/10/2019 14:05
    """
    return datetime.datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M")


def write_last_log_to_csv(source_log, output):
    """Функция получает на вход записи журнала с изменениями имен пользователей.
    Из всех представленных записей отбираются уникальные и актуальные.
    По завершении работы данные записываются в файл формата CSV

    Args:
        source_log (str): Имя CSV-файла с исходными данными
        output (str): Имя результирующего CSV-файла
    """
    with open(os.path.join(PATH, source_log)) as f:
        data = csv.DictReader(f)
        result_data = []
        for row in data:
            row['Last Changed'] = convert_str_to_datetime(row['Last Changed'])
            result_data.append(row)
            
    result_data = sorted(result_data, key=lambda d: d['Last Changed'])
    # pprint(result_data)
    result_data.reverse()
    uniq_mail_list = set()
    with open(os.path.join(PATH, output), 'w') as of:
        fieldnames = ['Name', 'Email', 'Last Changed']
        wr = csv.DictWriter(of, fieldnames)
        wr.writeheader()
        for item in result_data:
            if item['Email'] not in uniq_mail_list:
                uniq_mail_list.add(item['Email'])
                item['Last Changed'] = convert_datetime_to_str(item['Last Changed'])
                wr.writerow(item)
                

if __name__ == "__main__":
    write_last_log_to_csv("mail_log.csv", "output.csv")