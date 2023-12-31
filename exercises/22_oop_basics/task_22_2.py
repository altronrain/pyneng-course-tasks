# -*- coding: utf-8 -*-

"""
Задание 22.2

Создать класс CiscoTelnet, который подключается по Telnet к оборудованию Cisco.

При создании экземпляра класса, должно создаваться подключение Telnet, а также
переход в режим enable.
Класс должен использовать модуль telnetlib для подключения по Telnet.

У класса CiscoTelnet, кроме __init__, должно быть, как минимум, два метода:
* _write_line - принимает как аргумент строку и отправляет на оборудование строку
  преобразованную в байты и добавляет перевод строки в конце. Метод _write_line должен
  использоваться внутри класса.
* send_show_command - принимает как аргумент команду show и возвращает вывод
  полученный с оборудования
* close - закрывает Telnet сессию

Параметры метода __init__:
* ip - IP-адрес
* username - имя пользователя
* password - пароль
* secret - пароль enable

Пример создания экземпляра класса:
In [2]: from task_22_2 import CiscoTelnet

In [3]: r1_params = {
   ...:     'ip': '192.168.139.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}
   ...:

In [4]: r1 = CiscoTelnet(**r1_params)

In [5]: r1.send_show_command("sh ip int br")
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.139.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                unassigned      YES manual up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nR1#'


Подсказка:
Метод _write_line нужен для того чтобы можно было сократить строку:
self.telnet.write(line.encode("ascii") + b"\n")

до такой:
self._write_line(line)

Он не должен делать ничего другого.
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
    r1 = CiscoTelnet(**r1_params)
    pprint(r1.send_show_command("sh ip int br"))
    r1.close()