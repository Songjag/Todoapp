import sqlite3

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
        if data and data[0] == password:
            return True
        return False

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


    def close(self):
        self.conn.close()

class TodoList:
    def __init__(self):
        self.database=sqlite3.connect('user.db')
        self.cursor = self.database.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todolist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                work TEXT NOT NULL,
                FOREIGN KEY (user) REFERENCES users(user)
            )
        ''')
        self.database.commit()
    def add_work(self,user,work):
        self.cursor.execute('insert into user(user,work) values (?,?)',(user,work))
        self.database.commit()
    def done_work(self,user,work):
        self.cursor.execute('delete from todolist where user=? and work=?',(user,work))
        self.database.commit()

    def get_work(self,user):
        data=self.cursor.execute('SELECT work from todolist where user=?',(user))
        work_list=data.fetchall()
        return work_list