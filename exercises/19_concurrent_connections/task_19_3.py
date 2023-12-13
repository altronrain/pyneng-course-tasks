# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_command_to_devices, которая отправляет разные
команды show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом
команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands

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


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    """Функция выполняет переданные команды на указанных устройствах.
    Результат выполнения команды записывается в файл.

    Args:
        devices (list): Список устройств для обработки
        commands_dict (dict): Словарь команд для выполнения на устройствах
        filename (str): Имя файла для записи результатов
        limit (int, optional): Количество потоков для вычислений. Defaults to 3.
    """
    with ThreadPoolExecutor(max_workers=limit) as ex:
        task_queue = []
        for device in devices:
            host = device['host']
            task = ex.submit(send_show_command, device, commands_dict[host])
            task_queue.append(task)
    with open(p/filename, 'a') as f:
        for task in task_queue:
            f.write(f'{task.result()}\n')


if __name__ == "__main__":
    # Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
    # тест берет адреса из файла devices.yaml
    commands = {
        "192.168.139.3": "sh run | s ^router ospf",
        "192.168.139.1": "sh ip int br",
        "192.168.139.2": "sh int desc",
    }
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_command_to_devices(devices, commands, 'output2.txt')
    
