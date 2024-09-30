from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.s3_utils import download_db_from_s3, upload_db_to_s3, get_db_connection
from tracking.main import EmployeeAgent


auth_bp = Blueprint('auth_bp', __name__)

active_agents = {}




#homePage
@auth_bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')



# Signup route
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            flash('Email already registered!', 'danger')
        else:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()

            # Upload the updated database back to S3
            upload_db_to_s3()

            flash('Account created successfully!', 'success')
            return redirect(url_for('auth_bp.login'))

        conn.close()

    return render_template('signup.html')

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('user_bp.dashboard'))
        else:
            flash('Invalid email or password', 'danger')

        conn.close()

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'default_user')
    agent = active_agents.pop(username, None)
    if agent:
        agent.stop()
    session.clear()
    return redirect(url_for('auth_bp.login'))
