# -*- coding: utf-8 -*-
"""
Задание 11.1a

Создать функцию convert_mac_list которая конвертирует список MAC-адресов из
разных форматов в 1a:1b:2c:2d:3e:3f.

Конвертация MAC-адресов должна выполняться с помощью функции convert_mac из
задания 11.1. При этом нельзя копировать код функции convert_mac.

У функции convert_mac_list должно быть два параметра:
* mac_list - ожидает как аргумент список с MAC-адресами
* strict - параметр, который контролирует, что делать с неправильными
  MAC-адресами. Возможные значения True/False. Значение по умолчанию False.

Если все MAC-адреса правильные, функция должна вернуть список этих же
MAC-адресов, но в формате 1a:1b:2c:2d:3e:3f. Если какие-то MAC-адреса
неправильные (функция convert_mac сгенерировала исключение ValueError), в
зависимости от параметра strict надо:
* если strict равен True - не перехватывать исключение ValueError из функции
  convert_mac
* если strict равен False - игнорировать неправильные MAC-адреса и добавить в
  список только те, которые прошли проверку

Пример работы функции:

In [9]: convert_mac_list(["1a1b.2c2d.3e3f", "111122223333", "1111-2222-3333"], strict=False)
Out[9]: ['1a:1b:2c:2d:3e:3f', '11:11:22:22:33:33', '11:11:22:22:33:33']

In [10]: convert_mac_list(["1a1b.2c2d.3e3f", "1111WWWW3333", "1111-2222-3333"], strict=False)
Out[10]: ['1a:1b:2c:2d:3e:3f', '11:11:22:22:33:33']

In [11]: convert_mac_list(["1a1b.2c2d.3e3f", "1111WWWW3333", "1111-2222-3333"], strict=True)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Input In [11], in <cell line: 1>()
----> 1 convert_mac_list(["1a1b.2c2d.3e3f", "1111WWWW3333", "1111-2222-3333"], strict=True)
...
ValueError: '1111WWWW3333' does not appear to be a MAC address
"""
from task_11_1 import convert_mac

def convert_mac_list(mac_list, strict=False):
    """
    Функция обрабатывает список MAC-адресов, преобразуя их к виду 'aa:bb:cc:11:22:33'

    Params:
        mac_list (list): Список MAC-адресов для обрабротки
        strict (bool): Режим обработки:
                True -- вызывать ошибку при обнаружении некорректного MAC-адреса;
                False -- игнорировать некорректный MAC-адрес.  

    Returns:
        list: Список MAC-адресов в новом предствалении
    """
    new_mac_list = []
    for mac_addr in mac_list:
        try:
            convert_mac(mac_addr)
        except ValueError:
            if strict:
                raise
        else:
            new_mac_list.append(convert_mac(mac_addr))
    return new_mac_list    
