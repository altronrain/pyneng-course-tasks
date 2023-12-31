# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.139.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.139.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.139.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""
#import os
from time import sleep
from telnetlib import Telnet
from textfsm import clitable
from pathlib import Path
from pprint import pprint

#PATH = '/home/altron/Documents/repos/pyneng-course-tasks/exercises/22_oop_basics/'

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
            enable_output = self._read_until_prompt()
            if 'Password' in enable_output:
                raise ConnectionError(f'Enable authentication failed on device {self.ip}')
            self._write_line('terminal length 0')
            self._read_until_prompt()
        except OSError as error:
            print(error)
        
    
    def _write_line(self, line):
        return self._telnet.write(line.encode('ascii') + b"\n")
    
    def _read_until_prompt(self):
        return self._telnet.read_until(b'#').decode('ascii')
    
    def send_show_command(
        self, command,
        parse=True,
        templates='templates',
        index='index'
        ):
        self._write_line(command)
        sleep(self.pause)
        if parse:
            #cli = clitable.CliTable(index, os.path.join(PATH, templates))
            cli = clitable.CliTable(index, templates)
            cmd_output = self._read_until_prompt()
            cli.ParseCmd(cmd_output, {'Command': command})
            headers = cli.header
            return [dict(zip(headers, list(row))) for row in cli]
        else:
            return self._read_until_prompt()
    
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
    pprint(r1.send_show_command("sh ip int br", parse=True))
    pprint(r1.send_show_command("sh ip int br", parse=False))
    r1.close()