from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['DATABASE'] = 'your_database.db'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # Use a stronger hashing method in production


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        cur = g.db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        g.db.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        cur = g.db.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cur.fetchone()
        if user:
            session['user_id'] = user[0]
            flash('Login successful.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)


