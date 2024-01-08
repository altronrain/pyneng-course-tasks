import re
import yaml
import sqlite3
from pathlib import Path

p = Path('.')

def fill_devices_table(database_name, switches_info_filename):
    print('Добавляю данные в таблицу switches...')
    con = sqlite3.connect(database_name)
    insert_sql = "INSERT into switches values (:hostname, :location)"
    with open(switches_info_filename) as d:
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

def fill_interfaces_table(database_name, snooping_file_list):
    print('Добавляю данные в таблицу dhcp...')
    update_dhcp_active_column(database_name)
    con = sqlite3.connect(database_name)
    insert_sql = """
    INSERT or REPLACE into dhcp values (?, ?, ?, ?, ?, "1", datetime('now'))
    """
    for snooping_f in snooping_file_list:
        device = snooping_f.name.split("_")[0]
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


if __name__ == '__main__':
    db_name = 'dhcp_snooping.db'
    switches_info = 'switches.yml'
    snooping_files = sorted(list(p.glob('*dhcp_snooping.txt')))
    snooping_files_new = sorted(list(p.glob('new_data/*dhcp_snooping.txt')))
    # fill_devices_table(db_name, switches_info)
    fill_interfaces_table(db_name, snooping_files)
    #fill_interfaces_table(db_name, snooping_files_new)