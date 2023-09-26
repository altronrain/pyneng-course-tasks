# -*- coding: utf-8 -*-
"""
Задание 5.5a

Дополнить скрипт из задания 5.5 таким образом, чтобы, в зависимости
от выбранного режима, задавались разные вопросы в запросе о номере
VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Плюсом будет решить задание без использования условия if и цикла for,
но первый вариант решения лучше сделать так, как будет получаться.
"""

access_template = """switchport mode access
switchport access vlan {}
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
"""

trunk_template = """switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan {}
"""

mode = input("Введите режим работы интерфейса (access/trunk): ")
iface = input("Введите тип и номер интерфейса: ")

vlans_dict = { "access" : "Введите номер VLAN: ", "trunk": "Введите разрешенные VLANы: "}
vlans = input(vlans_dict[mode])

switch_dict = { "access" : access_template.format(vlans), "trunk" : trunk_template.format(vlans)}

print(f"interface {iface}")
print(switch_dict[mode])