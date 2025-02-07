import sqlite3

def initiate_db():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
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
	connection.close()
	
def is_included(username):
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	cursor.execute(f"SELECT username FROM Users WHERE username == ?", (username,))

	if cursor.fetchone() is not None:
		connection.close()
		return True
	else:
		connection.close()
		return False

	
def add_user(username, email, age):
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	if not is_included(username):
		cursor.execute("INSERT INTO Users (username,email,age,balance) VALUES (?,?,?,?)",(username,email,age,1000))
		connection.commit()
		connection.close()
	
def add_in_db():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	cursor.execute("INSERT INTO Products (title,description,price) VALUES (?,?,?)", ('Balance','Amazfit Balance','17000'))
	cursor.execute("INSERT INTO Products (title,description,price) VALUES (?,?,?)",('T-Rex 3','Amazfit T-Rex 3','23000'))
	connection.commit()
	connection.close()


def get_all_products():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	products=cursor.execute("SELECT * FROM Products").fetchall()
	connection.commit()
	connection.close()
	return products



