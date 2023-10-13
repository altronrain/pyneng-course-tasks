# -*- coding: utf-8 -*-
"""
Задание 9.5a

Сделать копию функции generate_trunk_config из задания 9.5

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
- ключи: имена интерфейсов, вида 'FastEthernet0/1'
- значения: список команд, который надо выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_dict и шаблона trunk_cmd_list.

Пример работы функции
In [2]: pprint(generate_trunk_config(trunk_dict, trunk_cmd_list))
{'FastEthernet0/1': ['switchport mode trunk',
                     'switchport trunk native vlan 999',
                     'switchport trunk allowed vlan 10,20,30'],
 'FastEthernet0/2': ['switchport mode trunk',
                     'switchport trunk native vlan 999',
                     'switchport trunk allowed vlan 11,30'],
 'FastEthernet0/4': ['switchport mode trunk',
                     'switchport trunk native vlan 999',
                     'switchport trunk allowed vlan 17']}

В заданиях 9го раздела и дальше, кроме указанной функции можно создавать любые
дополнительные функции.
"""
from pprint import pprint

def generate_trunk_config(intf_vlan_dict, trunk_template):
    """
    Функция генерирует конфигурацию для настройки trunk-портов

    Params:
        intf_vlan_dict (dict): Словарь соответствия "интерфейс"-"vlans"
        trunk_template (list): Список команд для настройки интерфейса

    Returns:
        dict:  Словарь соответствия "интерфейс"-"команды". Команды представлены в виде списка.
    """
    intf_cmds_dict = {}
    for intf, vlans_list in intf_vlan_dict.items():
        intf_cmds_dict[intf]=[]
        # Преобразование списка vlans к нужному виду:    
        vlans = str(vlans_list).strip("[]").replace(" ","")
        for command in trunk_template:
            if command.endswith("allowed vlan"):
                intf_cmds_dict[intf].append(f"{command} {vlans}")
            else:
                intf_cmds_dict[intf].append(command)
    return intf_cmds_dict 


trunk_cmd_list = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_dict = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}

pprint(generate_trunk_config(trunk_dict, trunk_cmd_list))