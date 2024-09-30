from flask import Blueprint, render_template, request, redirect, url_for, session
from tracking.activity_tracker import ActivityTracker, ScreenshotManager 
from utils.s3_utils import get_db_connection, upload_db_to_s3
import time
from tracking.main import EmployeeAgent

# Define the blueprint for user-related routes
user_bp = Blueprint('user_bp', __name__)


# Global variables to store tracker instances
activity_tracker_instance = None
screenshot_manager_instance = None

# Route for rendering the dashboard
@user_bp.route('/dashboard')
def dashboard():
    """Render the dashboard page for the logged-in user."""
    if 'user_id' in session:
        return render_template('dashboard.html')  # Render the dashboard for logged-in user
    return redirect(url_for('auth.login'))  # Redirect to login if user is not authenticated


@user_bp.route('/start-day', methods=['POST'])
def start_day():
    global activity_tracker_instance, screenshot_manager_instance

    if 'user_id' in session:
        user_id = session['user_id']

        def log_activity(mouse_activity=None, keyboard_activity=None, screenshot_path=None):
            conn = get_db_connection()
            conn.execute('INSERT INTO activity_log (user_id, mouse_activity, keyboard_activity, screenshot_path) VALUES (?, ?, ?, ?)', 
                         (user_id, mouse_activity, keyboard_activity, screenshot_path))
            conn.commit()
            conn.close()
            upload_db_to_s3()  # Sync the updated database to S3

        def upload_to_s3(screenshot_path):
            # Logic to upload screenshots to S3 can be added here if needed
            pass

        # Create instances of trackers
        activity_tracker_instance = ActivityTracker(user_id=user_id, log_callback=log_activity)
        screenshot_manager_instance = ScreenshotManager(user_id=user_id, log_callback=log_activity, upload_callback=upload_to_s3)

        # Start tracking
        activity_tracker_instance.start_tracking()
        screenshot_manager_instance.start_capturing()

        # Store flags in session to indicate that tracking is active
        session['is_tracking'] = True

        return redirect(url_for('user_bp.dashboard'))

    return "Not logged in", 403

@user_bp.route('/stop-day', methods=['POST'])
def stop_day():
    global activity_tracker_instance, screenshot_manager_instance

    if 'is_tracking' in session and session['is_tracking']:
        # Stop tracking using the instance
        if activity_tracker_instance is not None:
            activity_tracker_instance.stop_tracking()
        
        if screenshot_manager_instance is not None:
            screenshot_manager_instance.stop_capturing()

        # Clear tracking flag from session
        session.pop('is_tracking', None)

        return redirect(url_for('user_bp.dashboard'))

    print("Tracking was expected to be started, but session does not contain tracking instances.")
    return "Tracking not started", 403




# Route to handle user logout
@user_bp.route('/logout')
def logout():
    """Log the user out and clear the session."""
    session.clear()  # Clear all session data
    return redirect(url_for('auth.login'))  # Redirect to the login page after logging out

# Route to handle user login (assuming there's a form with 'username' and 'password')
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login and session creation."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate the login credentials (assuming there's a users table with username and password)
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            # Set the user_id in the session to log in the user
            session['user_id'] = user['id']
            session['username'] = user['username']

            session['is_admin'] = user['is_admin']
            return redirect(url_for('user_bp.dashboard'))  # Redirect to the dashboard after successful login
        else:
            # Invalid credentials, return an error message or redirect
            return "Invalid credentials", 403

    return render_template('login.html')  # Render the login page for GET requests



@user_bp.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    """Render the admin dashboard with user activity logs."""
    if 'is_admin' not in session or not session['is_admin']:
        return "Access denied", 403  # Ensure the user is an admin
    
    conn = get_db_connection()
    activities = conn.execute('SELECT * FROM activity_log ORDER BY timestamp DESC').fetchall()  # Fetch all activity logs
    conn.close()
    
    return render_template('admin_dashboard.html', activities=activities)


# Route to handle user registration
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Insert the new user into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('user.login'))  # Redirect to the login page after registration

    return render_template('register.html')  # Render the registration page for GET requests
