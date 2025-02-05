import sqlite3
'''	
initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
title(название продукта) - текст (не пустой)
description(описание) - текст
price(цена) - целое число (не пустой)
'''


def initiate_db():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Products(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	description TEXT,
	price INTEGER NOT NULL 
	);
	''')
	connection.commit()
	connection.close()
	
def add_in_db():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	cursor.execute("INSERT INTO Products (title,description,price) VALUES (?,?,?)", ('Forerunner 55','Garmin Forerunner 55','22800'))
	cursor.execute("INSERT INTO Products (title,description,price) VALUES (?,?,?)",('Watch GS 3','HONOR Watch GS 3','12000'))
	connection.commit()
	connection.close()

'''
get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

'''


def get_all_products():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	products=cursor.execute("SELECT * FROM Products").fetchall()
	connection.commit()
	connection.close()
	return products