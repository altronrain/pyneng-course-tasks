import sqlite3
from pathlib import Path

def create_db_tables(database_name, schema_str):
    con = sqlite3.connect(database_name)
    con.executescript(schema_str)
    con.close()

if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    db_schema_file = 'dhcp_snooping_schema.sql'
    with open(db_schema_file) as s:
        db_struct = s.read()
    if Path(db_name).is_file():
        print('База данных существует')
    else:
        print('Создаю базу данных...')
        create_db_tables(db_name, db_struct)