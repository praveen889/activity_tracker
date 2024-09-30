from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.s3_utils import get_db_connection, upload_db_to_s3
from datetime import datetime, timedelta
import os

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin_users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password))
        conn.commit()
        conn.close()

        upload_db_to_s3()

        return redirect(url_for('admin_bp.admin_login'))

    return render_template('admin_signup.html')


@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_users WHERE email = ? AND password = ?", (email, password))
        admin_user = cursor.fetchone()
        conn.close()

        if admin_user:
            session['admin_logged_in'] = True
            session['admin_username'] = admin_user['username']
            flash('Login successful. Redirecting to admin dashboard.', 'success')
            return redirect(url_for('admin_bp.admin_dashboard')) 
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('admin_login.html')

@admin_bp.route('/admin_logout')
def admin_logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('auth.admin_login'))

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    # # Fetch user activity data from the database
    # conn = get_db_connection()
    # # Fetch all users (assuming `users` table contains `username` and `email`)
    # users = conn.execute('SELECT id, username, email FROM users').fetchall()
    # conn.close()

    # # Render the admin dashboard with users' data
    # return render_template('admin_dashboard.html', users=users)

    # Check if the admin user is logged in
    if not session.get('admin_logged_in'):
        flash('You need to log in as an admin to access the dashboard.', 'danger')
        return redirect(url_for('admin.admin_login'))

    # Fetch data and render dashboard as before
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', users=users, username=session['admin_username'])


def calculate_activity_times(activity_logs):
    active_time = 0
    inactive_time = 0
    is_inactive = False
    last_timestamp = None

    for log in activity_logs:
        if log['mouse_activity'] is None and log['keyboard_activity'] is None:
            # If we were previously active, count the time as inactive
            if not is_inactive:
                if last_timestamp is not None:
                    inactive_time += (log['timestamp'] - last_timestamp).total_seconds()
                is_inactive = True
        else:
            # If we find any activity
            if is_inactive:
                # If we were inactive, we need to add time since last activity to active time
                if last_timestamp is not None:
                    active_time += (log['timestamp'] - last_timestamp).total_seconds()
                is_inactive = False
            
        last_timestamp = log['timestamp']

    return active_time, inactive_time



@admin_bp.route('/view_user_activity/<int:user_id>')
def view_user_activity(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user activity logs from the database
    cursor.execute("SELECT timestamp, mouse_activity, keyboard_activity FROM activity_log WHERE user_id = ? ORDER BY timestamp", (user_id,))
    activity_logs = cursor.fetchall()

    # Prepare the activity log data for processing, converting strings to datetime
    logs = []
    for row in activity_logs:
        timestamp = datetime.fromisoformat(row['timestamp'])  # Convert string to datetime
        logs.append({
            'timestamp': timestamp,
            'mouse_activity': row['mouse_activity'],
            'keyboard_activity': row['keyboard_activity']
        })

    # Calculate total active and inactive times
    active_time, inactive_time = calculate_activity_times(logs)

    # Fetch screenshots related to the user's activity
    cursor.execute("SELECT screenshot_path FROM activity_log WHERE user_id = ?", (user_id,))
    screenshots = [os.path.basename(row['screenshot_path']) for row in cursor.fetchall() if row['screenshot_path']]
    conn.close()

    return render_template('user_activity.html', user_id=user_id, active_time=int(active_time), inactive_time=int(inactive_time), screenshots=screenshots)
