# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

"""
arg_list = ["Prefix", "AD/Metric", "Next-Hop", "Last update", "Outbound Interface"]

with open("ospf.txt") as f:
    for line in f:
        route = line.replace(",", " ").replace("[", "").replace("]", "")
        r = route.split()
        # sorted_r = [r[1], r[2], r[4], r[5], r[6]]
        # И если бы умели (уже) итерировать по двум спискам:
        # for (i1, i2) in zip(arg_list, sorted_r):
        #     print(f"{i1:22}{i2}")
        # print("")
        print(f"{arg_list[0]:22}{r[1]}\n"
              f"{arg_list[1]:22}{r[2]}\n"
              f"{arg_list[2]:22}{r[4]}\n"
              f"{arg_list[3]:22}{r[5]}\n"
              f"{arg_list[4]:22}{r[6]}\n")
