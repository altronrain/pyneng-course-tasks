import re
import yaml
import sqlite3
from tabulate import tabulate
from datetime import timedelta, datetime

def create_db_from_output(database_name, schema_str):
    con = sqlite3.connect(database_name)
    con.executescript(schema_str)
    con.close()


def create_db(database_name, schema_file):
    with open(schema_file) as s:
        s_output = s.read()
    create_db_from_output(database_name, s_output)
    

def add_data_switches(database_name, switches_info_filename):
    con = sqlite3.connect(database_name)
    insert_sql = "INSERT into switches values (:hostname, :location)"
    with open(switches_info_filename[0]) as d:
        reader = yaml.safe_load(d)
        with con:
            for data_row in reader['switches'].items():
                try:
                    con.execute(insert_sql, data_row)
                except sqlite3.IntegrityError as error:
                    print(f'При добавлении данных: {data_row} Возникла ошибка: {error}')
    con.close()


def parse_dhcp_snooping(output):
    regex = re.compile(
        r"(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)"
    )
    result_list = []
    for line in output.split("\n"):
        match_ = regex.search(line)
        if match_:
            result_list.append(match_.groups())
    return result_list


def update_dhcp_active_column(database_name):
    con = sqlite3.connect(database_name)
    update_sql = 'UPDATE dhcp set active = "0"'
    with con:
        con.execute(update_sql)
    con.close()
    
def delete_week_old_records(database_name):
    con = sqlite3.connect(database_name)
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    delete_sql = 'DELETE from dhcp WHERE last_active < ?'
    with con:
        con.execute(delete_sql, (week_ago, ))
    con.close()
        

def add_data(database_name, snooping_file_list):
    update_dhcp_active_column(database_name)
    delete_week_old_records(database_name)
    con = sqlite3.connect(database_name)
    insert_sql = """
    INSERT or REPLACE into dhcp values (?, ?, ?, ?, ?, "1", datetime('now'))
    """
    for snooping_f in snooping_file_list:
        device = snooping_f.split("_")[0]
        with open(snooping_f) as f:
            out = f.read()
        parsed_out = parse_dhcp_snooping(out)
        for mac, ip, vlan, iface in parsed_out:
            data_row = (mac, ip, vlan, iface, device)
            with con:
                try:
                    con.execute(insert_sql, data_row)
                except sqlite3.IntegrityError as error:
                    print(f'При добавлении данных: {data_row} Возникла ошибка: {error}')
    con.close()
    
def get_table_headers(connection, table_name):
    select_headers = f'select name from pragma_table_info("{table_name}")'
    headers = []
    for row in connection.execute(select_headers):
        headers.extend(row)
    return headers


def format_and_print_output(rows_list):
    active = [row for row in rows_list if row[-2] == 1]
    non_active = [row for row in rows_list if row[-2] == 0]
    print('Активные записи:')
    print(tabulate(active))
    if non_active:
        print('Нективные записи:')
        print(tabulate(non_active))
        
def get_all_data(database_name):
    con = sqlite3.connect(database_name)
    select_dhcp_all = "SELECT * from dhcp order by active"
    dhcp_list = list(con.execute(select_dhcp_all))
    format_and_print_output(dhcp_list)
    con.close()


def get_data(database_name, param_name, param_value):
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
        format_and_print_output(dhcp_list)
    con.close()