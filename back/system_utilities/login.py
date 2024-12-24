from werkzeug.security import check_password_hash
from back.system_utilities.system import System

class LoginSystem(System):
    def login_user(self, email, password):
        cursor = self.db.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[1], password):
            user_id = user[0]
            self.log_activity(user_id, 'login', f'User with email {email} logged in')
            return True
        else:
            print("Error: Invalid email or password")
            return False

    def get_user_id(self, email):
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        return user[0] if user else None