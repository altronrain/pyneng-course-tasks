# -*- coding: utf-8 -*-
"""
Задание 7.2b

Скопировать код из задания 7.2a и переделать его: вместо вывода на стандартный
поток вывода, скрипт должен записать полученные строки в файл.

Имена файлов нужно передавать как аргументы скрипту:
1 аргумент имя исходного файла конфигурации
2 аргумент имя итогового файла конфигурации, в который будут записаны строки

Пример вызова:
$ python task_7_2b.py config_sw1.txt new_config.txt

При этом, должны быть отфильтрованы строки со словами, которые содержатся в списке ignore
и строки, которые начинаются на '!'.
"""
import sys
ignore = ["duplex", "alias", "configuration", "end", "service"]

with open(sys.argv[1]) as src, open(sys.argv[2], "w") as dst:
    for line in src:
        word_present = False
        if not line.startswith("!"):
            for word in ignore:
                if word in line:
                    word_present = True
            if not word_present:
                dst.write(line)