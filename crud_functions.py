import sqlite3
'''	

'''
connection = sqlite3.connect('database.db')
cursor = connection.cursor()
'''
is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.
'''

def initiate_db():
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Products(
	id PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	description TEXT,
	price INTEGER NOT NULL 
	);
	''')
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Users(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	email TEXT NOT NULL,
	age INTEGER NOT NULL,
	balance INTEGER NOT NULL 
	);
	''')
	connection.commit()
	
def is_included(username):
	cursor.execute(f"SELECT username FROM Users WHERE username == {username}").fetchall()
	
def add_user(username, email, age):
	cursor.execute("INSERT INTO Users (username,email,age,balance) VALUES (?,?,?,?)",(username,email,age,1000))
	connection.commit()
	
def add_in_db():
	cursor.execute("INSERT INTO Products (title,description,price) VALUES (?,?,?)", ('Balance','Amazfit Balance','17000'))
	cursor.execute("INSERT INTO Products (title,description,price) VALUES (?,?,?)",('T-Rex 3','Amazfit T-Rex 3','23000'))
	connection.commit()

'''
get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

'''


def get_all_products():
	products=cursor.execute("SELECT * FROM Products").fetchall()
	connection.commit()
	return products

connection.commit()
#connection.close()
