import sqlite3 as sq
from datetime import date, timedelta, datetime
from typing import Any


try:
    db = sq.connect('./utils/langBotDatabase.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    print('utils')
    for i in data:
        print(i)
except sq.OperationalError:
    print('error')