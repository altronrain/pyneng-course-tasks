# -*- coding: utf-8 -*-
"""
Задание 20.2

Создать шаблон templates/cisco_router_base.txt.

В шаблон templates/cisco_router_base.txt должно быть включено содержимое шаблонов:
* templates/cisco_base.txt
* templates/alias.txt
* templates/eem_int_desc.txt

При этом, нельзя копировать текст шаблонов.

Проверьте шаблон templates/cisco_router_base.txt, с помощью
функции generate_config из задания 20.1. Не копируйте код функции generate_config.

В качестве данных, используйте информацию из файла data_files/router_info.yml

"""
import yaml
from pathlib import Path
from task_20_1 import generate_config

p = Path('exercises/20_jinja2')
# так должен выглядеть вызов функции
if __name__ == "__main__":
    data_file = p/"data_files/router_info.yml"
    template_file = p/"templates/cisco_router_base.txt"
    with open(data_file) as f:
        data = yaml.safe_load(f)
    print(generate_config(template_file, data))
