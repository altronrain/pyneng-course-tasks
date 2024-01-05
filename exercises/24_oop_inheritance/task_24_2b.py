# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.139.1 возникла ошибка "Incomplete command."


Тесты в этом разделе проверяют подключение на устройствах в файле devices.yaml.
Если параметры подключения к вашим устройствам отличаются, надо изменить
параметры в файле devices.yaml.
"""
import re
from _collections_abc import Iterable
from netmiko.cisco.cisco_ios import CiscoIosSSH

class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """

class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()
        
    def _check_error_in_command(self, command, output):
        regex = r'((:?Invalid input detected|Incomplete command|Ambiguous command).+)\n*'
        match_ = re.search(regex, output)
        if match_:
            raise ErrorInCommand(
                f'При выполнении команды "{command}" на устройстве {self.host}'
                f' возникла ошибка {match_.group()}'
                                 )
    
    def send_command(self, command):
        output = super().send_command(command)
        self._check_error_in_command(command, output)
        return output
    
    def send_config_set(self, commands):
        if isinstance(commands, str):
            commands = [commands, 'end']
        commands = [*commands, 'end']
        output = ''
        for cmd in commands:
            part = super().send_config_set(cmd, exit_config_mode=False)
            self._check_error_in_command(cmd, part)
            output += part
        return output
    
if __name__ == "__main__":
    device_params = {
        "device_type": "cisco_ios",
        "ip": "192.168.139.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    r1 = MyNetmiko(**device_params)
    # print(r1.send_config_set(['logging buffered 20010', 'ip http server']))
    print(r1.send_config_set('lo'))
    
