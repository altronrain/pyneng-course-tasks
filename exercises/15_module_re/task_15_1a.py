# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

Пример вызова функции
In [2]: get_ip_from_cfg("config_r1.txt")
Out[2]:
{'Loopback0': ('10.1.1.1', '255.255.255.255'),
 'Ethernet0/0': ('10.0.13.1', '255.255.255.0'),
 'Ethernet0/2': ('10.0.19.1', '255.255.255.0')}

"""
import re
import os
from pprint import pprint

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/15_module_re"

# finditer
def get_ip_from_cfg(filename):
    """Функция обрабатывает переданный ей конфигурационный файл
    и формирует словарь с ключами в виде имен интерфейсов.
    Значения представляют собой кортежи из IP-адресов и масок, присутствующих
    на интерфейсах, описанных в файле конфигурации.

    Params:
        filename (str): Имя файла конфигурации для дальнейшей обработки

    Returns:
        dict: Словарь, содержащий сведения об адресации на интерфейсах
        Формат словаря: { 'Interface':('IP-address', 'Netmask'), ...} 
    """
    intf_dict = {}
    regex = r"interface (\S+).+? ip address ([0-9.]+) ([0-9.]+)"
    with open(os.path.join(PATH, filename)) as f:
        output = f.read()
    
    rmatch = re.finditer(regex, output, re.DOTALL)
    for m in rmatch:
        #print(m.groups())
        intf = m.group(1)
        ip_mask = m.groups()[1:]
        intf_dict[intf] = ip_mask
    
    return intf_dict

# search
def get_ip_from_cfg(filename):
    """Функция обрабатывает переданный ей конфигурационный файл
    и формирует словарь с ключами в виде имен интерфейсов.
    Значения представляют собой кортежи из IP-адресов и масок, присутствующих
    на интерфейсах, описанных в файле конфигурации.

    Params:
        filename (str): Имя файла конфигурации для дальнейшей обработки

    Returns:
        dict: Словарь, содержащий сведения об адресации на интерфейсах
        Формат словаря: { 'Interface':('IP-address', 'Netmask'), ...} 
    """
    intf_dict = {}
    regex = r"^interface (\S+)|^ ip address ([0-9.]+) ([0-9.]+)"
    with open(os.path.join(PATH, filename)) as f:
        for line in f:
            rmatch = re.search(regex, line)
            if rmatch:
                #print(rmatch.lastindex)
                if rmatch.lastindex == 1:
                    intf = rmatch.group(1)
                else:
                    intf_dict[intf] = rmatch.groups()[1:]
    return intf_dict

if __name__ == "__main__":
    pprint(get_ip_from_cfg("config_r1.txt"))