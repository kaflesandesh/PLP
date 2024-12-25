from werkzeug.security import check_password_hash
from back.system_utilities.system import System
from flask import request

class LoginSystem(System):
    def login_user(self, username, password):
        cursor = self.db.cursor()
        ip_address = request.remote_addr

        if username:
            cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[1], password):
                user_id = user[0]
                self.log_activity(user_id, 'login', f'User ** logged in from IP {ip_address}')
                return True
            else:
                self.log_activity(None, 'failed_login', f'Failed login attempt for username {username} from IP {ip_address}')
                print("Error: Invalid username or password")
                return False
        else:
            self.log_activity(None, 'failed_login', f'Failed login attempt with no username from IP {ip_address}')
            print("Error: No username provided")
            return False

    def get_user_id(self, username):
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        return user[0] if user else None