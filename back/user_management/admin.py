from back.user_management.user import User

class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)

    def manage_user_accounts(self):
        pass  # Add logic for managing accounts

    def generate_reports(self):
        pass  # Add logic for generating system reports
