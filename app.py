from datetime import timedelta, datetime, timezone
from langchain_ollama import OllamaLLM
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from back.system_utilities.dbmanage import User, create_tables_if_not_exist, get_db
from back.system_utilities.user import login_required, user_bp
from back.course import course_bp
from back.chatbot import chatbot_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3) 

# Register the blueprints
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(course_bp, url_prefix='/course')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

# Create database tables if they do not exist
create_tables_if_not_exist()

# Initialize the Ollama LLM
llm = OllamaLLM(model="gemma3:4b", temperature=0.7)

@app.context_processor
def inject_user():
    return dict(username=session.get('username', 'Guest'))

@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True
    session['last_activity'] = datetime.now(timezone.utc)

@app.before_request
def check_inactivity():
    last_activity = session.get('last_activity')
    if last_activity:
        now = datetime.now(timezone.utc)
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

@app.route('/course/courses')
@login_required
def courses():
    return render_template('courses.html')

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

@app.route("/chatbot")
def chatbot():
    return render_template("base.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
