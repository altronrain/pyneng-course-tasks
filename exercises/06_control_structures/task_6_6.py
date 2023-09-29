# -*- coding: utf-8 -*-
"""
Задание 6.6

Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
В зависимости от типа адреса (описаны ниже), вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223 (пример адреса 50.1.1.1)
   'multicast' - если первый байт в диапазоне 224-239 (пример адреса 224.1.1.1)
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях

Пример выполнения скрипта:
$ python task_6_6.py
Введите IP-адрес: 10.1.1.1
unicast

$ python task_6_6.py
Введите IP-адрес: 224.1.1.1
multicast

$ python task_6_6.py
Введите IP-адрес: 0.0.0.0
unassigned

$ python task_6_6.py
Введите IP-адрес: 255.255.255.255
local broadcast

$ python task_6_6.py
Введите IP-адрес: 250.1.1.1
unused

"""
ip_addr = input("Введите IP-адрес: ")
octets = ip_addr.split(".")

o1, o2, o3, o4 = [
    int(octets[0]),
    int(octets[1]),
    int(octets[2]),
    int(octets[3]),
]

if o1 == o2 == o3 == o4 == 0:
   print("unassigned")
elif o1 == o2 == o3 == o4 == 255:
   print("local broadcast")
elif o1 in range(1,224):
   print("unicast")
elif o1 in range(224,240):
   print("multicast")
else:
   print("unused")