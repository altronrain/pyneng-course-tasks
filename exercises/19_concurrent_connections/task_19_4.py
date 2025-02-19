# -*- coding: utf-8 -*-
"""
Задание 19.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config
на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* filename - имя файла, в который будут записаны выводы всех команд
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию None)
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Аргументы show, config и limit должны передаваться только как ключевые. При передачи
этих аргументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands_to_devices(devices, 'result.txt', 'sh clock')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands_to_devices(devices, 'result.txt', 'sh clock')

TypeError: send_commands_to_devices() takes 2 positional argument but 3 were given


При вызове функции send_commands_to_devices, всегда должен передаваться
только один из аргументов show, config. Если передаются оба аргумента, должно
генерироваться исключение ValueError.


Вывод команд должен быть записан в файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, 'result.txt', show='sh clock')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

In [13]: send_commands_to_devices(devices, 'result.txt', config=commands)

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.

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
    """Функция выполняет переданную show-команду на удаленном устройстве

    Args:
        device (dict): Словарь с параметрами подключения к устройству
        command (str): Команда для выполнения

    Returns:
        str: Вывод команды, включая приглашение на ввод
    """
    with Netmiko(**device) as cssh:
        cssh.enable()
        output = cssh.send_command(command)
        hostname = cssh.find_prompt()
    return f"{hostname}{command}\n{output}\n"


def send_config_commands(device, commands):
    """Функция выполняет переданную config-команду на удаленном устройстве

    Args:
        device (dict): Словарь с параметрами подключения к устройству
        command (str): Команда для выполнения

    Returns:
        str: Вывод команды, включая приглашение на ввод
    """
    with Netmiko(**device) as cssh:
        cssh.enable()
        output = cssh.send_config_set(commands, strip_command=False)
        hostname = cssh.find_prompt()
    return f"{hostname}{output}\n"


def send_commands_to_devices(devices, filename, *, show=None, config=None, limit=3):
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
            if show  and config:
                raise ValueError('Переданы оба типа аргументов')
            elif config:
                task = ex.submit(send_config_commands, device, config)
                task_queue.append(task)
            elif show:
                task = ex.submit(send_show_command, device, show)  
                task_queue.append(task)              
            elif not show and not config:
                raise ValueError('Не было передано ни одной команды')
    with open(p/filename, 'a') as f:
        for task in task_queue:
            f.write(f'{task.result()}')


if __name__ == "__main__":
    # Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
    # тест берет адреса из файла devices.yaml
    commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_commands_to_devices(devices, 'result.txt', show='sh clock')
    send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')
    send_commands_to_devices(devices, 'result.txt', config=commands)