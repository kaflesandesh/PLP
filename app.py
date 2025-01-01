from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from back.system_utilities.user import user_bp
from back.system_utilities.dbmanage import User, create_tables_if_not_exist, get_db
from transformers import pipeline
from functools import wraps
from datetime import timedelta, datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3) 

# Load the small LLM (Flan-T5)
chatbot_model = pipeline("text2text-generation", model="google/flan-t5-small")

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')

# Create database tables if they do not exist
create_tables_if_not_exist()

@app.context_processor
def inject_user():
    return dict(username=session.get('username', 'Guest'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to view this page.', 'warning')
            return redirect(url_for('user.login')) 
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True
    session['last_activity'] = datetime.utcnow()

@app.before_request
def check_inactivity():
    last_activity = session.get('last_activity')
    if last_activity:
        now = datetime.utcnow()
        if (now - last_activity).total_seconds() > app.config['PERMANENT_SESSION_LIFETIME'].total_seconds():
            session.clear()
            flash('You have been logged out due to inactivity.', 'warning')
            return redirect(url_for('user.login'))

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/courses')
@login_required
def courses():
    user_type = session.get('user_type', 'guest')
    return render_template('courses.html', user_type=user_type)

@app.route('/assignments')
@login_required
def assignments():
    return render_template('assignments.html')

@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html')

@app.route('/materials')
@login_required
def materials():
    return render_template('materials.html')

@app.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "")
    user_id = session.get("user_id", None)

    user_type = "guest"
    db = next(get_db())
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user_type = user.type

    context = f"You are assisting a {user_type}. "
    response = chatbot_model(context + user_message, max_length=100, num_return_sequences=1, clean_up_tokenization_spaces=True)
    reply = response[0]['generated_text']
    db.close()

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
