import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

class System:
    def __init__(self, db_path='plp.db'):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.db:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                )
            ''')
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    middle_name TEXT,
                    dob TEXT NOT NULL,
                    address TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id)
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
        cursor.execute('SELECT * FROM registrations WHERE email = ?', (email,))
        return cursor.fetchone() is not None

    def generate_username(self, first_name):
        random_number = random.randint(10, 99)  # Generate a random 2-digit number
        return f"{first_name}{random_number}"

    def register_user(self, first_name, last_name, middle_name, dob, address, email, phone, password):
        if self.validate_user(email):
            print(f"Error: User with email {email} already exists.")
            return

        username = self.generate_username(first_name)
        password_hash = generate_password_hash(password)
        try:
            with self.db:
                self.db.execute('''
                    INSERT INTO users (username, password_hash)
                    VALUES (?, ?)
                ''', (username, password_hash))
                user_id = self.db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
                self.db.execute('''
                    INSERT INTO registrations (first_name, last_name, middle_name, dob, address, email, phone, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (first_name, last_name, middle_name, dob, address, email, phone, user_id))
                self.log_activity(user_id, 'register', f'User {username} registered with email {email}')
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

    def log_activity(self, user_id, activity_type, description):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute('''
            INSERT INTO logs (timestamp, user_id, activity_type, description)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, user_id, activity_type, description))
        self.db.commit()

    def list_users(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT username, email FROM registrations')
        return cursor.fetchall()

    def get_logs(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT timestamp, user_id, activity_type, description FROM logs')
        return cursor.fetchall()
