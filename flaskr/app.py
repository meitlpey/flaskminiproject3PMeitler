from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from db import get_db, close_db, init_db
from auth import hash_password

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Set the database path
app.config['DATABASE'] = 'path_to_your_database_file.db'

# Initialize the database
init_db()

@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
            db.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

        flash(error, 'error')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash('Login successful.', 'success')
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
