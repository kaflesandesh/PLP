import random
from flask import Blueprint, redirect, request, jsonify, session, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from back.system_utilities.dbmanage import User, UserInformation, get_db, Log
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

user_bp = Blueprint('user', __name__)

def log_activity(db, user_id, activity_type, message):
    """
    Logs user activity in the database using ORM.
    """
    try:
        log_entry = Log(user_id=user_id, action=activity_type, message=message)
        db.add(log_entry)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error logging activity: {e}")
        
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
        else:
            data = request.form

        username = data.get('username')
        password = data.get('password')
        ip_address = request.remote_addr

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        db = next(get_db())
        try:
            user = db.query(User).filter(User.username == username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_type'] = user.type
                log_activity(db, user.id, 'login', f'User logged in from IP {ip_address}')
                return redirect(url_for('dashboard'))
            log_activity(db, None, 'failed_login', f'Invalid login attempt for {username} from {ip_address}')
            return jsonify({"message": "Invalid credentials"}), 401
        finally:
            db.close()
    return render_template('login.html')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        required_fields = ['first_name', 'email', 'password', 'user_type']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({"message": f"Missing fields: {', '.join(missing_fields)}"}), 400
        
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        last_name = data.get('last_name')
        dob = data.get('dob')
        address = data.get('address')
        email = data.get('email')
        password = data.get('password')
        major = data.get('major')
        user_type = data.get('user_type')
        phone = data.get('phone')

       # Convert dob to date object
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400
        
        db = next(get_db())
        try:
            existing_user = db.query(UserInformation).filter(UserInformation.email == email).first()
            if existing_user:
                return jsonify({"message": "Email is already registered"}), 400

            hashed_password = generate_password_hash(password)
            username = first_name + str(random.randint(10, 99))

            new_user = User(username=username, password=hashed_password, type=user_type)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            new_user_info = UserInformation(
                user_id=new_user.id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                dob=dob,
                address=address,
                email=email,
                major=major,
                phone=phone
            )
            db.add(new_user_info)
            db.commit()

            log_activity(db, new_user.id, 'register', f'New user registered with email {email}')
            return jsonify({"message": "Registration successful"}), 201
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error during registration: {e}")
            return jsonify({"message": "An error occurred during registration"}), 500
        finally:
            db.close()
    return render_template('register.html')
