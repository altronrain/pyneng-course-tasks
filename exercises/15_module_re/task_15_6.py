# -*- coding: utf-8 -*-
"""
Задание 15.6

Создать функцию convert_mac которая конвертирует mac-адрес из разных форматов в
1a:1b:2c:2d:3e:3f.
У функции должен быть один параметр: mac_address, который ожидает строку с
MAC-адресом в одном из форматов ниже.  Функция должна возвращать строку с
MAC-адресом в формате 1a:1b:2c:2d:3e:3f.

Должна поддерживаться конвертация из таких форматов:
* 1a1b2c2d3e3f
* 1a1b:2c2d:3e3f
* 1a1b.2c2d.3e3f
* 1a-1b-2c-2d-3e-3f
* 1a.1b.2c.2d.3e.3f
* 1a1b-2c2d-3e3f
* 1a:1b:2c:2d:3e:3f (оставить без изменений)

Функция также должна проверять, что строка, которая была передана функции,
содержит правильный MAC-адрес. MAC-адрес считается правильным, если:
- каждый символ, кроме разделителей ":-.", это символ в диапазоне a-f, A-F или 0-9
- не считая разделители, в MAC-адресе должно быть 12 символов

Если как аргумент была передана строка, которая не содержит правильный
MAC-адрес, сгенерировать исключение ValueError (... должно быть заменено на
переданное значение, примеры ниже): ValueError: '...' does not appear to be a
MAC address

Проверить работу функции на разных MAC-адресах в списке mac_list.

Пример работы функции:

In [1]: convert_mac("1a1b.2c2d.3e3f")
Out[1]: '1a:1b:2c:2d:3e:3f'

In [2]: convert_mac("1A1B.2C2D.3E3F")
Out[2]: '1A:1B:2C:2D:3E:3F'

In [3]: convert_mac("1111.2222.3333")
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
import re
import os
from pprint import pprint

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/15_module_re"

def convert_mac(mac):
    """
    Функция производит преобразование представления MAC-адресов.

    Params:
        mac (str): Передаваемый MAC-адрес

    Returns:
        str: MAC-адрес вида "aa:aa:bb:bb:cc:cc"
    """
    #regex = r"(([a-fA-F0-9]{2})([:.-]?)){6}"
    """ RE работает, но в случае его применения у нас не получится
    на лету собрать новый MAC. Придется прибегать к методам строк и т.д."""
    regex = (
        r"([a-fA-F0-9]{2})[:.-]?([a-fA-F0-9]{2})[:.-]?"
        r"([a-fA-F0-9]{2})[:.-]?([a-fA-F0-9]{2})[:.-]?"
        r"([a-fA-F0-9]{2})[:.-]?([a-fA-F0-9]{2})"
    )
    rmatch = re.fullmatch(regex, mac)
    if rmatch:
        #print(rmatch.groups())
        new_mac = (":").join(rmatch.groups()).lower()
    else:
        raise ValueError(f"{mac} does not appear to be a MAC address")
    return new_mac


if __name__ == "__main__":
    pprint(convert_mac("1A1B.2C2D.3E3F"))