import sqlite3

def run_sql_script(db_path, script_path):
    conn = sqlite3.connect(db_path)
    with open(script_path, 'r') as file:
        sql_script = file.read()
    try:
        conn.executescript(sql_script)
        print(f'Executed {script_path} successfully.')
    except Exception as exception:
        print(f'Error executting {script_path}: {exception}')
    finally:
        conn.close()

if __name__ == '__main__':
    db_file = 'development.db'
    run_sql_script(db_file, 'generate_tables.sql')
    run_sql_script(db_file, 'init_data.sql')