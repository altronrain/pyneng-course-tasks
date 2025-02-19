# -*- coding: utf-8 -*-
"""
Задание 19.3a

Создать функцию send_command_to_devices, которая отправляет список указанных
команд show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке,
но вывод команд с одного устройства должен идти по порядку.
Например, для словаря commands и устройства 192.168.100.1 сначала должен быть
вывод sh ip int br, потом sh int desc.


Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой
команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Для выполнения задания можно создавать любые дополнительные функции,
а также использовать функции созданные в предыдущих заданиях.

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
            for cmd in commands_dict[host]:
                task = ex.submit(send_show_command, device, cmd)
                task_queue.append(task)
    with open(p/filename, 'a') as f:
        for task in task_queue:
            f.write(f'{task.result()}\n')


if __name__ == "__main__":
    # Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
    # тест берет адреса из файла devices.yaml
    commands = {
        "192.168.139.3": ["sh ip int br", "sh ip route | ex -"],
        "192.168.139.1": ["sh ip int br", "sh int desc"],
        "192.168.139.2": ["sh int desc"],
    }
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_command_to_devices(devices, commands, 'output3.txt')
