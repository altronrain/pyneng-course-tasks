# -*- coding: utf-8 -*-
"""
Задание 20.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt
и данных из файла data_files/for.yml.

Важный нюанс: надо получить каталог из параметра template и использовать его, нельзя
указывать текущий каталог в FileSystemLoader - то есть НЕ надо делать так FileSystemLoader(".").
Указание текущего каталога, сломает работу других заданий/тестов.
"""
import os
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

p = Path('exercises/20_jinja2')

def generate_config(template, data_dict):
    template_dir, template_file = os.path.split(template)
    # template_dir = template.parent
    # template_file = template.name
    env = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True
    )
    cfg_template = env.get_template(template_file)
    return cfg_template.render(data_dict)
    
    
# так должен выглядеть вызов функции
if __name__ == "__main__":
    data_file = p/"data_files/for.yml"
    template_file = p/"templates/for.txt"
    with open(data_file) as f:
        data = yaml.safe_load(f)
    print(generate_config(template_file, data))
