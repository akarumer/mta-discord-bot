# ztoohn
import pymysql
import sqlite3

'''Внешняя база данных'''
connection = pymysql.connect(
    host='162.19.126.72',
    port=3306,
    user='gs74885',
    passwd='hb29kk4w',
    database='gs74885'
)

'''Локальная база данных 2'''
# connectionl = pymysql.connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     passwd='',
#     database='nrp'
# )

'''Локальная база данных 1'''
db = sqlite3.connect('mta-grand/dbs/users.db')

'''Промокоды'''
promodb = sqlite3.connect('mta-grand/dbs/promocodes.db')