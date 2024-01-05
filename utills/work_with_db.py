from main import cursor, conn


async def check_table_userid(id):
    table_name = f"user_{id}"
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
        name TEXT UNIQUE,
        date VARCHAR(5),
        remember_date VARCHAR(5));
        """)
    conn.commit()


async def add_new_remember(all_info, id):
    table_name = f"user_{id}"
    cursor.execute(f'INSERT INTO {table_name} (name, date, remember_date) VALUES ( ?, ?, ?)', (all_info['name'], all_info['date'], all_info['remember_date']))
    conn.commit()


async def get_all_birthday(id, name=None):
    table_name = f"user_{id}"
    if name is None:
        cursor.execute(f'SELECT * FROM {table_name};')
    else:
        cursor.execute(f'SELECT * FROM {table_name} WHERE name=="{name}";')
    rows = cursor.fetchall()
    return rows


async def check_edit_birthday(name, id):
    table_name = f"user_{id}"
    try:
        cursor.execute(f'SELECT * FROM {table_name} WHERE name == "{name}";')
        if cursor.fetchall()[0]:
            return True
        else:
            return False
    except BaseException:
        return False


async def edit_info_birthday(id, old_name, date, remember_date, new_name=None):
    table_name = f"user_{id}"
    if new_name is None:
        new_name = old_name
    try:
        cursor.execute(
            f'UPDATE {table_name} SET name = "{new_name}", date = "{date}", remember_date = "{remember_date}" WHERE name == "{old_name}";')
        conn.commit()
        return True
    except BaseException:
        return False
