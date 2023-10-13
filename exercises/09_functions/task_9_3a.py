# -*- coding: utf-8 -*-
"""
Задание 9.3a

Создать функцию clean_config.  Функция clean_config обрабатывает
конфигурационный файл и возвращает список команд из указанного
конфигурационного файла.

У функции clean_config должны быть такие параметры:
* config_filename - ожидает как аргумент имя конфигурационного файла
* ignore_lines - ожидает как аргумент список строк, которые надо игнорировать.
  Значение по умолчанию None. То есть по умолчанию никакие строки не игноруются
* ignore_exclamation - контролирует то игнорируются ли строки, которые
  начинаются с восклицательного знака. Возможные значения True/False.
  Значение по умолчанию True
* strip_lines - контролирует удаление пробела в начале строки и перевода строки в конце.
  True - удалить пробелы в начале строки и перевод в конце, False - не удалять.
  Возможные значения True/False. Значение по умолчанию False
* delete_empty_lines - контролирует удаление пустых строк. True - удалять, False - нет.
  Возможные значения True/False. Значение по умолчанию True

Для удобства все значения по умолчанию для необязательных параметров:
* ignore_lines - None
* ignore_exclamation - True
* delete_empty_lines - True
* strip_lines - False

Функция clean_config обрабатывает конфигурационный файл и возвращает список
команд из указанного конфигурационного файла:
* если в параметр ignore_lines передан список строк - исключая строки конфигурации,
  в которых содержатся строки из списка ignore_lines.
* если ignore_exclamation равно True - исключая строки которые начинаются с '!'
* если delete_empty_lines равно True - исключая пустые строки
* если strip_lines равно True - строки в списке должны быть без пробелов в начале
  и перевода строки в конце строки


Пример работы функции:
In [3]: clean_config("config_r3_short.txt", strip_lines=True, ignore_lines=ignore_list, ignore_exclamation=False)
Out[3]:
['hostname PE_r3',
 '!',
 'no ip http server',
 'no ip http secure-server',
 'ip route 10.2.2.2 255.255.255.255 Tunnel0',
 '!',
 '!',
 'ip prefix-list TEST seq 5 permit 10.6.6.6/32',
 '!',
 '!',
 '!',
 'alias configure sh do sh',
 '!',
 'line con 0',
 'exec-timeout 0 0',
 'privilege level 15',
 'logging synchronous']

In [4]: clean_config("config_r3_short.txt", strip_lines=True, ignore_lines=ignore_list)
Out[4]:
['hostname PE_r3',
 'no ip http server',
 'no ip http secure-server',
 'ip route 10.2.2.2 255.255.255.255 Tunnel0',
 'ip prefix-list TEST seq 5 permit 10.6.6.6/32',
 'alias configure sh do sh',
 'line con 0',
 'exec-timeout 0 0',
 'privilege level 15',
 'logging synchronous']

In [5]: clean_config("config_r3_short.txt", strip_lines=True, delete_empty_lines=False)
Out[5]:
['hostname PE_r3',
 '',
 'no ip http server',
 'no ip http secure-server',
 'ip route 10.2.2.2 255.255.255.255 Tunnel0',
 '',
 'ip prefix-list TEST seq 5 permit 10.6.6.6/32',
 '',
 'alias configure sh do sh',
 'alias exec ospf sh run | s ^router ospf',
 'alias exec bri show ip int bri | exc unass',
 'line con 0',
 'exec-timeout 0 0',
 'privilege level 15',
 'logging synchronous']


В заданиях 9го раздела и дальше, кроме указанной функции можно создавать любые
дополнительные функции.
"""
from pprint import pprint
import os

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/09_functions"

def ignore_line(line, ignore_lines):
    """
    Функция поиска игнорируемых слов из списка в составе строки.
    Если слов в строке не обнаружено - возвращаем False;
    Если при переборе слово найдено - возвращаем True.

    Params:
        line (str): Строка исходного файла конфигурации
        ignore_lines (list): Список игнорируемых слов 

    Returns:
        bool: Возвращает результат обнаружения игнорируемых слов в строке файла конффигурации
    """
    for ignore in ignore_lines:
        if ignore in line:
            return True
    return False


def clean_config(config_filename, ignore_lines=None, ignore_exclamation=True, delete_empty_lines=True, strip_lines=False):
    """
    Функция преобразования исходного файла конфигурации согласно заданным параметрам.
    Просмотр файла конфигурации производится построчно.
    Если строка удовлетворяет всем заданным условиям, то она записывается в результирующий список.
    
    Params:
        config_filename (str): Имя файла конфигурации, который будет обрабатываться
        ignore_lines (list, optional): Список слов, строки с которыми следует игнорировать. Defaults to None.
        ignore_exclamation (bool, optional): Задает правило обработки строк с "!". Defaults to True.
        delete_empty_lines (bool, optional): Задает правило обработки пустых строк. Defaults to True.
        strip_lines (bool, optional): Задает правило форматирования результирующих строк в списке. Defaults to False.

    Returns:
        list: Список строк, который был отобран из файла конфигурации.
    """
    cfg_list = []
    with open(os.path.join(PATH, config_filename)) as f:
        for line in f:
            good_line = True # маркер строки, удовлетворяющей условиям отбора
            if delete_empty_lines:
                good_line = line != "\n"
            if ignore_exclamation:
                good_line = "!" not in line and good_line
            if ignore_lines:
                good_line = not ignore_line(line, ignore_lines) and good_line
            if good_line:
                cfg_list.append(line.strip() if strip_lines else line)
    return cfg_list


ignore_list = ["duplex", "alias exec", "Current configuration", "service"]

pprint(clean_config("config_r3_short.txt", strip_lines=True, ignore_lines=ignore_list))
