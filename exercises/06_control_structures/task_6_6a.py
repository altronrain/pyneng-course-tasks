# -*- coding: utf-8 -*-
"""
Задание 6.6a

Сделать копию скрипта задания 6.6.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделены точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: "Неправильный IP-адрес".
Если адрес правильный, проверять и выводить тип адреса как в задании 6.6.

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Пример выполнения скрипта:
$ python task_6_6a.py
Введите IP-адрес: 10.10.1.1
unicast

$ python task_6_6a.py
Введите IP-адрес: 10.1.1
Неправильный IP-адрес

$ python task_6_6a.py
Введите IP-адрес: a.a.10.1
Неправильный IP-адрес

$ python task_6_6a.py
Введите IP-адрес: 50.1.a.a
Неправильный IP-адрес

$ python task_6_6a.py
Введите IP-адрес: 10,1,1,1
Неправильный IP-адрес

$ python task_6_6a.py
Введите IP-адрес: 500.1.1.1
Неправильный IP-адрес

$ python task_6_6a.py
Введите IP-адрес: 50.1.1.1.1
Неправильный IP-адрес
"""

ip_addr = input("Введите IP-адрес: ")
error = True

if ip_addr.count(".") == 3:
   octets = ip_addr.split(".")
   for num in octets:
      if not (num.isdigit() and int(num) in range(0,256)):
         error = True
         break
      else:
         error = False

if error:
   print("Неправильный IP-адрес")
else:
   o1, o2, o3, o4 = [
    int(octets[0]),
    int(octets[1]),
    int(octets[2]),
    int(octets[3]),
   ]
   
   if o1 == o2 == o3 == o4 == 0:
      print("unassigned")
   elif o1 == o2 == o3 == o4 == 255:
      print("local broadcast")
   elif o1 in range(1,224):
      print("unicast")
   elif o1 in range(224,240):
      print("multicast")
   else:
      print("unused")