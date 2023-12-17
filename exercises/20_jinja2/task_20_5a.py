# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве с
помощью netmiko.  Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel, который надо
использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять
ближайший свободный номер, но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel0, Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Проверить какие туннельные интерфейсы настроены на оборудовании можно, например,
командой sh ip int br или sh run.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import os
import re
import yaml
from netmiko import Netmiko
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pprint import pprint

p = Path('exercises/20_jinja2')

def send_show_command(device, command):
    """Функция выполняет переданную команду на удаленном устройстве

    Args:
        device (dict): Словарь с параметрами подключения к устройству
        command (str): Команда для выполнения

    Returns:
        str: Вывод команды
    """
    with Netmiko(**device) as cssh:
        cssh.enable()
        output = cssh.send_command(command)
    return output


def send_config_commands(device, commands):
    """Функция выполняет переданную config-команду на удаленном устройстве

    Args:
        device (dict): Словарь с параметрами подключения к устройству
        command (str): Команда для выполнения

    Returns:
        str: Вывод команды
    """
    with Netmiko(**device) as cssh:
        cssh.enable()
        output = cssh.send_config_set(commands)
    return output


def get_tuns(intf):
    """Функция обрабатывает вывод команды sh ip int br
    и возвращает найденные номера туннельных интерфейсов
    в случае их наличия

    Args:
        intf (str): Строка с выводом команды

    Returns:
        list: Список номеров туннельных интерфейсов
    """
    tuns = []
    regex = r'Tunnel(\d+)'
    rmatch = re.finditer(regex, intf, re.MULTILINE)
    for m in rmatch:
        tuns.append(int(m.group(1)))
    return tuns       

def find_tun_num(tuns1, tuns2):
    """Функция получает информацию о настроенных
    туннельных интерфейсах на конфигурируемых устройствах.
    Ищет свободный номер туннельного интерфейса на устройствах
    и возвращает его.

    Args:
        tuns1 (list): Список туннельных интерфейсов устройства 1
        tuns2 (list): Список туннельных интерфейсов устройства 2

    Returns:
        int: Номер свободного туннельного интерфейса
    """
    tun_num = 0
    if tuns1 is None and tuns2 is None:
        return tun_num
    tun_set = set(tuns1) | set(tuns2)
    while True:
        if tun_num in tun_set:
            tun_num += 1
        else:
            return tun_num


def create_vpn_config(template1, template2, data_dict):
    """Функция генерирует конфигурации IPSec для устройств
    на основе шаблонов и передаваемых параметров

    Args:
        template1 (str): Шаблон для устройства 1
        template2 (str): Шаблон для устройства 2
        data_dict (dict): Словарь с передаваемыми параметрами

    Returns:
        tuple: Конфигурации устройств
    """
    template_dir, template_file_1 = os.path.split(template1)
    _, template_file_2 = os.path.split(template2)
    # template_dir = template1.parent
    # template_file_1 = template1.name
    # template_file_2 = template2.name
    env = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True
    )
    cfg1 = env.get_template(template_file_1)
    cfg2 = env.get_template(template_file_2)
    return cfg1.render(data_dict), cfg2.render(data_dict)
      

def configure_vpn(
    src_device_params, dst_device_params,
    src_template, dst_template, vpn_data_dict
    ):
    """Функция конфигурирует на двух устройствах IPSec VPN.

    Args:
        src_device_params (dict): Параметры подключения к устройству 1
        dst_device_params (dict): Параметры подключения к устройству 2
        src_template (str): Шаблон для устройства 1
        dst_template (str): Шаблон для устройства 2
        vpn_data_dict (dict): Словарь с параметрами для шаблонов

    Returns:
        tuple: Вывод команд настройки с устройств
    """
    command = 'sh ip int br'
    src_intf = send_show_command(src_device_params, command)
    dst_intf = send_show_command(dst_device_params, command)
    vpn_data_dict['tun_num'] = find_tun_num(get_tuns(src_intf), get_tuns(dst_intf))
    src_conf, dst_conf = create_vpn_config(src_template, dst_template, vpn_data_dict)
    src_conf = src_conf.split('\n')
    dst_conf = dst_conf.split('\n')
    src_conf_output = send_config_commands(src_device_params, src_conf)
    dst_conf_output = send_config_commands(dst_device_params, dst_conf)
    return src_conf_output, dst_conf_output


if __name__ == "__main__":
    data = {
        "tun_num": None,
        "wan_ip_1": "192.168.100.1",
        "wan_ip_2": "192.168.100.2",
        "tun_ip_1": "10.0.1.1 255.255.255.252",
        "tun_ip_2": "10.0.1.2 255.255.255.252",
    }
    data_file = p/"data_files/for.yml"
    template1 = p/"templates/gre_ipsec_vpn_1.txt"
    template2 = p/"templates/gre_ipsec_vpn_2.txt"
    
    with open(p/"devices.yaml") as f:
        devices = yaml.safe_load(f)
    device1 = devices[0]
    device2 = devices[1]
    pprint(configure_vpn(device1, device2, template1, template2, data))
