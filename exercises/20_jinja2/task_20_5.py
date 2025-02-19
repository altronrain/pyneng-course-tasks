# -*- coding: utf-8 -*-
"""
Задание 20.5

Создать шаблоны templates/gre_ipsec_vpn_1.txt и templates/gre_ipsec_vpn_2.txt,
которые генерируют конфигурацию IPsec over GRE между двумя маршрутизаторами.

Шаблон templates/gre_ipsec_vpn_1.txt создает конфигурацию для одной стороны туннеля,
а templates/gre_ipsec_vpn_2.txt - для второй.

Примеры итоговой конфигурации, которая должна создаваться на основе шаблонов в файлах:
cisco_vpn_1.txt и cisco_vpn_2.txt.

Шаблоны надо создавать вручную, скопировав части конфига в соответствующие шаблоны.

Создать функцию create_vpn_config, которая использует эти шаблоны
для генерации конфигурации VPN на основе данных в словаре data.

Параметры функции:
* template1 - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* template2 - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна возвращать кортеж с двумя конфигурациями (строки),
которые получены на основе шаблонов.

Примеры конфигураций VPN, которые должна возвращать функция create_vpn_config в файлах
cisco_vpn_1.txt и cisco_vpn_2.txt.
"""
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pprint import pprint

p = Path('exercises/20_jinja2')

def create_vpn_config(template1, template2, data_dict):
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


if __name__ == "__main__":
    data = {
        "tun_num": 10,
        "wan_ip_1": "192.168.100.1",
        "wan_ip_2": "192.168.100.2",
        "tun_ip_1": "10.0.1.1 255.255.255.252",
        "tun_ip_2": "10.0.1.2 255.255.255.252",
    }
    data_file = p/"data_files/for.yml"
    template1 = p/"templates/gre_ipsec_vpn_1.txt"
    template2 = p/"templates/gre_ipsec_vpn_2.txt"
    pprint(create_vpn_config(template1, template2, data))
