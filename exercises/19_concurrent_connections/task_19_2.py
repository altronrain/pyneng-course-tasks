# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Подключение к оборудованию выполняется с помощью netmiko (SSH).

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml.

Тесты в этом разделе проверяют подключение на устройствах в файле devices.yaml.
Если параметры подключения к вашим устройствам отличаются, надо изменить
параметры в файле devices.yaml.
"""
import yaml
from pathlib import Path
from netmiko import Netmiko
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

p = Path('exercises/19_concurrent_connections')


def send_show_command(device, command):
    """Функция выполняет переданную команду на удаленном устройстве

    Args:
        device (dict): Словарь с параметрами подключения к устройству
        command (str): Команда для выполнения

    Returns:
        str: Вывод команды, включая приглашение на ввод
    """
    with Netmiko(**device) as cssh:
        cssh.enable()
        output = cssh.send_command(command, strip_command=False)
        hostname = cssh.find_prompt()
    return ''.join([hostname, output])


def send_show_command_to_devices(devices, command, filename, limit=3):
    """Функция выполняет переданную команду на группе устройств.
    Результат выполнения команды записывается в файл.

    Args:
        devices (list): Список устройств для обработки
        command (str): Команда для выполнения
        filename (str): Имя файла для записи результатов
        limit (int, optional): Количество потоков для вычислений. Defaults to 3.
    """
    with ThreadPoolExecutor(max_workers=limit) as ex:
        result = ex.map(send_show_command, devices, repeat(command))
    with open(p/filename, 'a') as f:
        for item in result:
            f.write(f'{item}\n')



if __name__ == "__main__":
    command = "sh ip int br"
    filename = 'output.txt'
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_show_command_to_devices(devices, command, 'output.txt')
