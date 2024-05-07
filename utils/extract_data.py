import sqlite3 as sq
from datetime import date, timedelta, datetime
from typing import Any

# try:
#     db = sq.connect('/home/topg/langbot/langbot-repo/secret/langBotDatabase.db')
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM users')
#     data = cursor.fetchall()
#     print('secret')
#     for i in data:
#         print(i)
# except sq.OperationalError:
#     print('error')
    
# print()

try:
    db = sq.connect('/home/topg/langbot/langbot-repo/utils/langBotDatabase.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    print('utils')
    for i in data:
        print(i)
except sq.OperationalError:
    print('error')
    
print()

# try:
#     db = sq.connect('/home/topg/langbot/langbot-repo/langBotDatabase.db')
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM users')
#     data = cursor.fetchall()
#     print('просто')
#     for i in data:
#         print(i)
# except sq.OperationalError:
#     print('error')