# -*- coding: utf-8 -*-
"""
Задание 18.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству
и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml
с помощью функции send_show_command (эта часть кода написана).

Тесты в этом разделе проверяют подключение на устройствах в файле devices.yaml.
Если параметры подключения к вашим устройствам отличаются, надо изменить
параметры в файле devices.yaml.
"""
import yaml
from pathlib import Path
from netmiko import Netmiko

p = Path('exercises/18_ssh_telnet')


def send_show_command(device, command):
    with Netmiko(**device) as cssh:
        output = cssh.send_command(command)
    return output


if __name__ == "__main__":
    command = "sh ip int br"
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
