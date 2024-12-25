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
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if system.login_user(username=username, password=password):
            user_id = system.get_user_id(username)
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        else:
            error = "Login failed. Please check your credentials."
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        dob = request.form['dob']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        system.register_user(first_name, last_name, middle_name, dob, address, email, phone, password)
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
