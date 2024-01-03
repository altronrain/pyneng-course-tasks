# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.139.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка

Тест проверяет подключение с параметрами из файла devices.yaml. Там должны быть
указаны доступные устройства.
"""
from time import sleep
from telnetlib import Telnet
from pprint import pprint

class CiscoTelnet:
    pause = 0.2
    timeout = 5
    
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        try:
            self._telnet = Telnet(self.ip, timeout=self.timeout)
            self._telnet.read_until(b'Username:')
            self._write_line(username)
            self._telnet.read_until(b'Password:')
            self._write_line(password)
            login_output = self._telnet.read_until(b'>', timeout=self.timeout).decode('ascii')
            if 'Login invalid' in login_output:
                raise ConnectionError(f'Authentication failed on device {self.ip}')
            self._write_line('enable')
            self._telnet.read_until(b'Password:')
            self._write_line(secret)
            enable_output = self._read_until_prompt().decode('ascii')
            if 'Password' in enable_output:
                raise ConnectionError(f'Enable authentication failed on device {self.ip}')
            self._write_line('terminal length 0')
            self._read_until_prompt()
        except OSError as error:
            print(error)
            
    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, ex_value, traceback):
        self.close()
        
    def _write_line(self, line):
        return self._telnet.write(line.encode('ascii') + b"\n")
    
    def _read_until_prompt(self):
        return self._telnet.read_until(b'#')
    
    def send_show_command(self, command):
        self._write_line(command)
        sleep(self.pause)
        return self._read_until_prompt().decode('ascii')
    
    def close(self):
        return self._telnet.close()

if __name__ == "__main__":
    r1_params = {
        'ip': '192.168.139.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
        }
    with CiscoTelnet(**r1_params) as r1:
        pprint(r1.send_show_command("sh ip int br"))
        #raise ValueError('Some error')