import sqlite3 as sq
from datetime import date, timedelta, datetime
from typing import Any

db = sq.connect('./utils/langBotDatabase.db')
cursor = db.cursor()


async def db_start():
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        pro BLOB DEFAULT 0,
        expire_date TEXT,
        does_dict_exists BLOB DEFAULT 0
    )''')
    print('users db are set')
    db.commit()
    await db_settings_start()


async def db_does_user_exist(user_id):
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    return True if len(cursor.fetchall()) == 1 else False


async def db_new_user(user_id, username, name):
    cursor.execute('INSERT INTO users (id, username, name) VALUES (?, ?, ?)', (user_id, username, name))
    db.commit()


async def db_change_name(name, user_id):
    cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
    db.commit()


# async def db_update_score(score, user_id):
#     cursor.execute('UPDATE users SET score = ? WHERE id = ?', (score, user_id))
#     db.commit()

async def db_check_pro(user_id):
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    pro = cursor.fetchone()
    print('pro', pro)
    if pro[3] == 0 and pro[4] is None:
        db.commit()
        return [False, None]
    else:
        cursor.execute('SELECT expire_date FROM users WHERE id = ?', (user_id,))
        expire_d = cursor.fetchone()
        print(expire_d)
        if pro[3] == 0: bool_ = False
        else: bool_ = True
        db.commit()
        return [bool_, expire_d]


async def db_update_pro(action, user_id):
    if action == 'get':
        cursor.execute('UPDATE users SET pro = 1 WHERE id = ?', (user_id,))
        td = timedelta(days=31)
        tod = date.today()
        d = tod
        print('today:', d)
        print('today:', td)
        expire_date = d + td
        cursor.execute('UPDATE users SET expire_date = ? WHERE id = ?', (expire_date, user_id))
        print('new pro sub')
    elif action == 'stop':
        cursor.execute('UPDATE users SET pro = 0 WHERE id = ?', (user_id,))
    elif action == 'extend':
        cursor.execute('SELECT expire_date FROM users WHERE id = ?', (user_id,))
        td = timedelta(days=31)
        dat = cursor.fetchone()
        d = datetime.strptime(dat[0], '%Y-%m-%d').date()
        print('today:', d)
        print('delta:', td)
        expire_date = d + td
        cursor.execute('UPDATE users SET expire_date = ? WHERE id = ?', (expire_date, user_id))
        print('extended pro sub')
    db.commit()


async def db_does_dict_exists(user_id):
    cursor.execute('SELECT does_dict_exists FROM users WHERE id = ?', (user_id,))
    does_dict = cursor.fetchone()
    print('does_dict', does_dict)
    if does_dict[0] == 0:
        db.commit()
        return False
    else:
        db.commit()
        return True



async def db_update_dict(user_id):
    cursor.execute('UPDATE users SET does_dict_exists = 1 WHERE id = ?', (user_id,))
    db.commit()


async def db_settings_start():
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        theme TEXT DEFAULT basic_theme,
        sys_lang TEXT DEFAULT english,
        camb_w_num INTEGER DEFAULT 0
    )''')
    print('settings are set')
    db.commit()


async def db_settings_first_set(user_id):
    cursor.execute('INSERT INTO settings (id) VALUES (?)', (user_id,))
    print('settings are inserted')
    db.commit()


async def db_settings_get_data(user_id):
    cursor.execute('SELECT * FROM settings WHERE id = ?', (user_id,))
    settings_data = cursor.fetchall()
    print('settings data:', settings_data[0])
    return [settings_data[0][1], settings_data[0][2]]


async def db_settings_get_theme(user_id):
    cursor.execute('SELECT theme FROM settings WHERE id = ?', (user_id,))
    settings_data = cursor.fetchall()
    print('settings data:', settings_data[0][0])
    return settings_data[0][0]


async def db_settings_get_camb_w_num(user_id):
    cursor.execute('SELECT camb_w_num FROM settings WHERE id = ?', (user_id,))
    settings_data = cursor.fetchall()
    print('settings data:', settings_data)
    return settings_data


async def db_settings_update_camb_w_num(user_id, num):
    cursor.execute('UPDATE settings SET camb_w_num = ? WHERE id = ?', (num, user_id))
    db.commit()


async def db_settings_update_theme(user_id, theme):
    cursor.execute('UPDATE settings SET theme = ? WHERE id = ?', (theme, user_id))
    print('theme updated')
    db.commit()
    print('идем дальше')