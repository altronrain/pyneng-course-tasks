# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.139.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
#import os
from time import sleep
from telnetlib import Telnet
from textfsm import clitable
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
            cli = clitable.CliTable(index, templates)
            cmd_output = self._read_until_prompt()
            cli.ParseCmd(cmd_output, {'Command': command})
            headers = cli.header
            return [dict(zip(headers, list(row))) for row in cli]
        else:
            return self._read_until_prompt()
        
    def send_config_commands(self, commands):
        if type(commands) == str:
            commands = ["conf t", commands, "end"]
        else:
            commands = ["conf t", *commands, "end"]
        output = ''
        for cmd in commands:
            self._write_line(cmd)
            sleep(self.pause)
            output += self._read_until_prompt()
        return output
        
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
    #pprint(r1.send_config_commands('logging 10.1.1.1'))
    pprint(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))
    r1.close()