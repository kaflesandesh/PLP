import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

class System:
    def __init__(self):
        self.db = sqlite3.connect('plp.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.db:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    user_type TEXT NOT NULL
                )
            ''')
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_id INTEGER,
                    activity_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

    def validate_user(self, email):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone() is not None

    def register_user(self, name, email, password, user_type):
        if self.validate_user(email):
            print(f"Error: User with email {email} already exists.")
            return

        password_hash = generate_password_hash(password)
        try:
            with self.db:
                self.db.execute('''
                    INSERT INTO users (name, email, password_hash, user_type)
                    VALUES (?, ?, ?, ?)
                ''', (name, email, password_hash, user_type))
                user_id = self.db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()[0]
                self.log_activity(user_id, 'register', f'User {name} registered with email {email}')
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

    def log_activity(self, user_id, activity_type, description):
        timestamp = datetime.now().isoformat()
        with self.db:
            self.db.execute('''
                INSERT INTO logs (timestamp, user_id, activity_type, description)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, user_id, activity_type, description))

    def list_users(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT name, email, user_type FROM users')
        return cursor.fetchall()

    def get_logs(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT timestamp, user_id, activity_type, description FROM logs')
        return cursor.fetchall()
