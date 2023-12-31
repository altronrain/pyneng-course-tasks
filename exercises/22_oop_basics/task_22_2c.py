# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.139.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.139.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.139.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.139.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.139.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
#import os
import re
from time import sleep
from telnetlib import Telnet
from textfsm import clitable

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
        
    def send_config_commands(self, commands, strict=True):
        if type(commands) == str:
            commands = ["conf t", commands, "end"]
        else:
            commands = ["conf t", *commands, "end"]
        output = ''
        for cmd in commands:
            self._write_line(cmd)
            sleep(self.pause)
            part = self._read_until_prompt()
            output += part
            if '%' in part:
                regex = r'% (.+?)\r\n'
                rmatch = re.finditer(regex, part)
                for m in rmatch:
                    error = m.group()
                error_msg = f'При выполнении команды {cmd} на устройстве {self.ip} возникла ошибка -> {error}'
                if strict:
                    raise ValueError(error_msg)
                else:
                    print(error_msg, end="")
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
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors+correct_commands
    print(r1.send_config_commands(commands, strict=True))
    r1.close()