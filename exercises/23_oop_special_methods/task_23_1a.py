# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
from pprint import pprint

class IPAddress:
    def __init__(self, ipaddr):
        if '/' not in ipaddr:
            raise ValueError('Incorrect input')
        ip, mask = ipaddr.split('/')    
        if type(ip) != str or len(ip.split('.')) != 4:
            raise ValueError('Incorrect IPv4 address')
        else:
            for octet in ip.split('.'):
                if not (octet.isdigit() and int(octet) in range(256)):
                    raise ValueError('Incorrect IPv4 address')
        
        if int(mask) not in range(8,33):
            raise ValueError('Incorrect mask')
        self.ip = ip
        self.mask = int(mask)
        
    def __str__(self):
        return f'IP address {self.ip}/{self.mask}'
    
    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"
        

if __name__ == "__main__":
    ip1 = IPAddress('10.1.1.1/24')
    print(ip1)
    pprint(ip1)