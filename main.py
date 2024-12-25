from flask import Flask, render_template, request, redirect, url_for, session
from back.system_utilities.login import LoginSystem

app = Flask(__name__)
app.secret_key = 'your_secret_key'
system = LoginSystem()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if system.login_user(email=email, password=password):
            user_id = system.get_user_id(email)
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        else:
            return "Login failed. Please check your credentials."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        system.register_user(name=name, email=email, password=password, user_type=user_type)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/courses')
def courses():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('courses.html')

@app.route('/assignments')
def assignments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('assignments.html')

@app.route('/progress')
def progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('progress.html')

@app.route('/materials')
def materials():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('materials.html')

@app.route('/feedback')
def feedback():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('feedback.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('feedback'))

if __name__ == "__main__":
    app.run(debug=True)
