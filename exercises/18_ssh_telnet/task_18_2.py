# -*- coding: utf-8 -*-
"""
Задание 18.2

Создать функцию send_config_commands

Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству и выполняет
перечень команд в конфигурационном режиме на основании переданных аргументов.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* config_commands - список команд, которые надо выполнить

Функция возвращает строку с результатами выполнения команды:

In [7]: r1
Out[7]:
{'device_type': 'cisco_ios',
 'ip': '192.168.100.1',
 'username': 'cisco',
 'password': 'cisco',
 'secret': 'cisco'}

In [8]: commands
Out[8]: ['logging 10.255.255.1', 'logging buffered 20010', 'no logging console']

In [9]: result = send_config_commands(r1, commands)

In [10]: result
Out[10]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.
         \nR1(config)#logging 10.255.255.1\nR1(config)#logging buffered 20010\n
         R1(config)#no logging console\nR1(config)#end\nR1#'

In [11]: print(result)
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.255.255.1
R1(config)#logging buffered 20010
R1(config)#no logging console
R1(config)#end
R1#


Скрипт должен отправлять команду command на все устройства из файла devices.yaml
с помощью функции send_config_commands.

Тесты в этом разделе проверяют подключение на устройствах в файле devices.yaml.
Если параметры подключения к вашим устройствам отличаются, надо изменить
параметры в файле devices.yaml.
"""
import yaml
from pathlib import Path
from netmiko import Netmiko
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoBaseException

p = Path('exercises/18_ssh_telnet')
commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]


def send_config_commands(device, config_commands):
    try:
        with Netmiko(**device) as cssh:
            cssh.enable()
            output = cssh.send_config_set(config_commands)
            return output
    except (SSHException, NetmikoBaseException) as error:
            print(f'{error}')


if __name__ == "__main__":
    command = "sh ip int br"
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_config_commands(dev, commands))