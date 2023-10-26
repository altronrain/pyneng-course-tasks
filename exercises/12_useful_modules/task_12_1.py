# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через
subprocess).  IP-адрес считается доступным, если выполнение команды ping
отработало с кодом 0 (returncode).  Нюансы: на Windows returncode может быть
равен 0 не только, когда ping был успешен, но для задания нужно проверять
именно код. Это сделано для упрощения тестов.

"""
import subprocess

def ping_ip_addresses(ip_list):
    """
    Функция проверяет доступность переданных ей IP-адресов.
    На основе выполнения данной проверки IP-адреса заносятся в два различных списка.
    (Для доступных и недоступных адресов).
    
    Params:
        ip_list (list): Список IP-адресов для проверки

    Returns:
        tuple: Кортеж из двух результирующих списков проверенных IP-адресов
        Первый список в составе коретжа -- для досупных IP-адресов;
        Второй -- для недоступных.
    """
    good_ip_list = []
    bad_ip_list = []
    process_list = []
    for ip in ip_list:
        process = subprocess.Popen(["ping", "-c", "1", ip],
                                   stderr=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL)
        process_list.append(process)
    for ip, pr in zip(ip_list, process_list):
        returncode = pr.wait()
        good_ip_list.append(ip) if returncode == 0 else bad_ip_list.append(ip)
    return (good_ip_list, bad_ip_list)