import sqlite3
import sys
from tabulate import tabulate


def get_table_headers(connection, table_name):
    select_headers = f'select name from pragma_table_info("{table_name}")'
    headers = []
    for row in connection.execute(select_headers):
        headers.extend(row)
    return headers


def format_and_print_output(rows_list):
    active = [row for row in rows_list if row[-1] == 1]
    non_active = [row for row in rows_list if row[-1] == 0]
    print('Активные записи:')
    print(tabulate(active))
    if non_active:
        print('Нективные записи:')
        print(tabulate(non_active))


def get_all_from_dhcp(database_name):
    con = sqlite3.connect(database_name)
    select_dhcp_all = "SELECT * from dhcp order by active"
    dhcp_list = list(con.execute(select_dhcp_all))
    format_and_print_output(dhcp_list)
    con.close()


def get_param_from_dhcp(database_name, param_name, param_value):
    con = sqlite3.connect(database_name)
    select_dict = {
        'mac': 'SELECT * from dhcp where mac = ? order by active',
        'ip': 'SELECT * from dhcp where ip = ? order by active',
        'vlan': 'SELECT * from dhcp where vlan = ? order by active',
        'interface': 'SELECT * from dhcp where interface = ? order by active',
        'switch': 'SELECT * from dhcp where switch = ? order by active'
    }
    select_dhcp = select_dict.get(param_name)
    headers_dhcp = get_table_headers(con, "dhcp")
    if select_dhcp is None:
        print(
            'Данный параметр не поддерживается.',
            f'Допустимые значения параметров: {", ".join(headers_dhcp)}'
              )
    else:
        dhcp_list = list(con.execute(select_dhcp, [param_value]))
        print(
            'Информация об устройствах ',
            f'с такими параметрами: {param_name} {param_value}')
        format_and_print_output(dhcp_list)
    con.close()


def print_tables(db_name, arg_list):
    if len(arg_list) == 0:
        get_all_from_dhcp(db_name)
    elif len(arg_list) == 2:
        param, value = arg_list
        get_param_from_dhcp(db_name, param, value)
    else:
        print('Пожалуйста, введите два или ноль аргументов')


if __name__ == '__main__':
    db_name = 'dhcp_snooping.db'
    arg_list = sys.argv[1:]
    print_tables(db_name, arg_list)