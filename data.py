import sqlite3
from datetime import datetime

class User:
    def __init__(self, db_path="database.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def check_valid_user(self, user):
        self.cursor.execute("SELECT user FROM users WHERE user = ?", (user,))
        data = self.cursor.fetchone()
        return data is not None

    def check_password(self, user, password):
        self.cursor.execute("SELECT password FROM users WHERE user = ?", (user,))
        data = self.cursor.fetchone()
        return data and data[0] == password

    def create_user(self, user, name, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (user, name, password) VALUES (?, ?, ?)",
                (user, name, password)
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_name(self, user):
        self.cursor.execute("SELECT name FROM users WHERE user = ?", (user,))
        data = self.cursor.fetchone()
        return data[0] if data else None

    def close(self):
        self.conn.close()


class TodoList:
    def __init__(self, db_path="database.db"):
        self.database = sqlite3.connect(db_path)
        self.cursor = self.database.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todolist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                work TEXT NOT NULL,
                date_of_work TEXT NOT NULL,
                FOREIGN KEY (user) REFERENCES users(user)
            )
        ''')
        self.database.commit()

    def add_work(self, user, work, date=None):
    
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            'INSERT INTO todolist (user, work, date_of_work) VALUES (?, ?, ?)',
            (user, work, date)
        )
        self.database.commit()

    def done_work(self, user, work):
        self.cursor.execute(
            'DELETE FROM todolist WHERE user = ? AND work = ?',
            (user, work)
        )
        self.database.commit()

    def get_work(self, user, date=None):
        if date:
            data = self.cursor.execute(
                'SELECT work, date_of_work FROM todolist WHERE user = ? AND date_of_work = ?',
                (user, date)
            )
        else:
            data = self.cursor.execute(
                'SELECT work, date_of_work FROM todolist WHERE user = ?',
                (user,)
            )
        return data.fetchall()

    def close(self):
        self.database.close()
