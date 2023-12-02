# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""
import csv
import re
import os

PATH = "/home/altron/Documents/repos/pyneng-course-tasks/exercises/17_serialization"

def write_dhcp_snooping_to_csv(filenames, output):
    """
    Функция принимает список файлов с выводами команды show dhcp snooping binding.
    На выходе формируется общий CVS файл с данными по шаблону.

    Args:
        filenames (list): Список файлов для обработки
        output (str): Имя результирующего файла CSV
    """
    regex = r"^([0-9A-Z:]+) +([0-9.]+).+?(\d+) +(FastEthernet\d/\d+)$"
    dhcp_snooping_list = []
    for file in filenames:
        sw_name = file.split("_")[0]
        with open(os.path.join(PATH, file)) as f:
            content = f.read()       
        rmatch = re.finditer(regex, content, re.MULTILINE)
        for m in rmatch:
            m_list = [ sw_name, *m.groups()]
            dhcp_snooping_list.append(m_list)
            # print(dhcp_snooping_list)
        
    headers = ['switch', 'mac', 'ip', 'vlan', 'interface']
    with open(os.path.join(PATH, output), mode="a") as of:
        wr = csv.writer(of)
        wr.writerow(headers)
        wr.writerows(dhcp_snooping_list)

    
if __name__ == "__main__":
    sh_dhcp_snoop_files = [
        "sw1_dhcp_snooping.txt",
        "sw3_dhcp_snooping.txt",
    ]
    write_dhcp_snooping_to_csv(sh_dhcp_snoop_files, "output.csv")