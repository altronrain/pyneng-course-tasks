# -*- coding: utf-8 -*-
"""
Задание 6.6b

Сделать копию скрипта задания 6.6a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'.
Сообщение "Неправильный IP-адрес" должно выводиться только один раз после
каждого ввода адреса, даже если несколько пунктов проверки адреса не выполнены
(пример вывода ниже).

Пример выполнения скрипта:
$ python task_6_6b.py
Введите IP-адрес: 10.1.1.1
unicast

$ python task_6_6b.py
Введите IP-адрес: a.a.a
Неправильный IP-адрес
Введите IP-адрес: 10.1.1.1.1
Неправильный IP-адрес
Введите IP-адрес: 500.1.1.1
Неправильный IP-адрес
Введите IP-адрес: a.1.1.1
Неправильный IP-адрес
Введите IP-адрес: 50.1.1.1
unicast

$ python task_6_6b.py
Введите IP-адрес: 10.a.1.1.1
Неправильный IP-адрес
Введите IP-адрес: 255.255.255.255
local broadcast

"""
error = True

while error:
    ip_addr = input("Введите IP-адрес: ")
    if ip_addr.count(".") == 3:
        octets = ip_addr.split(".")
        for num in octets:
            if not (num.isdigit() and int(num) in range(0,256)):
                error = True
                break
            else:
                error = False
    if error:
        print("Неправильный IP-адрес")

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