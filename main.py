from back.system_utilities.system import System

def main():
    system = System()

    # Register users in the database
    system.register_user(name="Admin User", email="admin@example.com", user_type="admin")
    system.register_user(name="John Doe", email="john.doe@example.com", user_type="student")
    system.register_user(name="Dr. Smith", email="dr.smith@example.com", user_type="instructor")

    # List all users
    print("Users registered in the system:")
    for user in system.list_users():
        print(f"- {user[0]} ({user[1]})")

if __name__ == "__main__":
    main()
