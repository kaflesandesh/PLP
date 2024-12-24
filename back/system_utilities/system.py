import sqlite3

class System:
    def __init__(self):
        self.db = sqlite3.connect('plp.db')
        self.create_tables()

    def create_tables(self):
        with self.db:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    user_type TEXT NOT NULL
                )
            ''')

    def register_user(self, name, email, user_type):
        try:
            with self.db:
                self.db.execute('''
                    INSERT INTO users (name, email, user_type)
                    VALUES (?, ?, ?)
                ''', (name, email, user_type))
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

    def list_users(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT name, email FROM users')
        return cursor.fetchall()
