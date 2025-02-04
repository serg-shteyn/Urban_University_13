#Домашнее задание по теме
# "Выбор элементов и функции в SQL запросах"


import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS  Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')
active = False

if active:
    for i in range(1,11):
        cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?,?,?,?)",
                       ('User'+str(i), 'example'+str(i)+'gmail.com', i*10, 1000 ))
if active:
    for i in range(1,11):
        if i%2:
            cursor.execute("UPDATE Users SET balance = ? WHERE username == ?" , (500,f"User{i}"))
n=1
if active:
    while n<=10:
        cursor.execute("DELETE FROM Users WHERE username == ?", (f"User{n}",))
        n+=3

#    Удалите из базы данных not_telegram.db запись с id = 6.
#cursor.execute("DELETE FROM Users WHERE id == ?", (6,))

#    Подсчитать общее количество записей.
cursor.execute("SELECT COUNT(*) FROM Users ")
total_users = cursor.fetchone()[0]

#    Посчитать сумму всех балансов.
cursor.execute("SELECT SUM(balance) FROM Users")
total_balance = cursor.fetchone()[0]

#    Вывести в консоль средний баланс всех пользователей.
avr_balance = total_balance/total_users
print(avr_balance)



connection.commit()
connection.close()
