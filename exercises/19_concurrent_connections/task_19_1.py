# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
import subprocess
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor

def ping_ip(ip):
    """Функция проверяет доступность переданного ей IP-адреса.
    Возвращает результат проверки.

    Args:
        ip (str): IP-адрес, требующий проверки

    Returns:
        int: Код возврата команды ping
    """
    process = subprocess.Popen(["ping", "-c", "1", ip],
                                stderr=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL)
    return process.wait()
    

def ping_ip_addresses(ip_list, limit=3):
    """
    Функция проверяет доступность переданных ей IP-адресов.
    На основе выполнения данной проверки IP-адреса заносятся в два различных списка.
    (Для доступных и недоступных адресов).
    
    Params:
        ip_list (list): Список IP-адресов для проверки
        limit (int): Количество потоков для вычислений

    Returns:
        tuple: Кортеж из двух результирующих списков проверенных IP-адресов
        Первый список в составе коретжа -- для досупных IP-адресов;
        Второй -- для недоступных.
    """
    good_ip_list = []
    bad_ip_list = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip, ip_list)
        for ip, rcode in zip(ip_list, result):
            good_ip_list.append(ip) if rcode == 0 else bad_ip_list.append(ip)
    return good_ip_list, bad_ip_list

if __name__ == "__main__":
    ip_list = ['192.168.139.1', '192.168.139.2',
               '192.168.139.3', '192.168.139.4',
               '192.168.139.5']
    pprint(ping_ip_addresses(ip_list, 5))