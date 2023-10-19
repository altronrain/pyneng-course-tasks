# -*- coding: utf-8 -*-
"""
Задание 11.1

Создать функцию convert_mac которая конвертирует mac-адрес из разных форматов в
1a:1b:2c:2d:3e:3f.
У функции должен быть один параметр: mac_address, который ожидает строку с
MAC-адресом в одном из форматов ниже.  Функция должна возвращать строку с
MAC-адресом в формате 1a:1b:2c:2d:3e:3f.

Должна поддерживаться конвертация из таких форматов:
* 1a1b2c2d3e3f
* 1a1b:2c2d:3e3f
* 1a1b.2c2d.3e3f
* 1a1b-2c2d-3e3f

Функция также должна проверять, что строка, которая была передана функции,
содержит правильный MAC-адрес. MAC-адрес считается правильным, если:
- каждый символ, кроме разделителей ":-.", это символ в диапазоне a-f или 0-9
- не считая разделители, в MAC-адресе должно быть 12 символов

Проверок выше достаточно для этого задания, то есть не обязательно проверять формат
адреса более точно.

Если как аргумент была передана строка, которая не содержит правильный
MAC-адрес, сгенерировать исключение ValueError (... должно быть заменено на
переданное значение, примеры ниже): ValueError: '...' does not appear to be a
MAC address

Проверить работу функции на разных MAC-адресах в списке mac_list.

Пример работы функции:

In [2]: convert_mac("1a1b.2c2d.3e3f")
Out[2]: '1a:1b:2c:2d:3e:3f'

In [3]: convert_mac("1111:2222:3333")
Out[3]: '11:11:22:22:33:33'

In [4]: convert_mac("111122223333")
Out[4]: '11:11:22:22:33:33'

In [5]: convert_mac("1111-2222-3333")
Out[5]: '11:11:22:22:33:33'

In [6]: convert_mac("1111-2222-33")
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Input In [6], in <cell line: 1>()
----> 1 convert_mac("1111-2222-33")
...
ValueError: '1111-2222-33' does not appear to be a MAC address


In [7]: convert_mac("1111-2222-33WW")
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Input In [7], in <cell line: 1>()
----> 1 convert_mac("1111-2222-33WW")
...
ValueError: '1111-2222-33WW' does not appear to be a MAC address

"""

def convert_mac(mac):
    """
    Функция производит преобразование представления MAC-адресов.

    Args:
        hwaddr (str): MAC-адрес вида "aaaa.bbbb.cccc"

    Returns:
        str: MAC-адрес вида "aa:aa:bb:bb:cc:cc"
    """
    check_str = set("0123456789abcdf")
    
    if not mac[4].isalpha(): # mac[4] -- possible delimeter
        tmp_mac = mac.replace(mac[4],"") 
    bad_mac = set(tmp_mac).difference(check_str)
    if len(mac) != 12 or bad_mac:
        raise ValueError(f"{mac} does not appear to be a MAC address")
    else:
        for i in range(len(tmp_mac)):
            if i > 0 and i % 2 == 0:
                new_mac = new_mac + ":"
            new_mac = new_mac + mac[i]
    return new_mac


correct_mac_example = [
    "111122223333",
    "1a1b.2c2d.3e3f",
    "1111-2222-3333",
]
wrong_mac_example = ["1a1b.rrrr.3e3f", "1111tttt3333", "1111-2222-33"]

