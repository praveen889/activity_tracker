# activity_tracker

#########################################
#                                       #
#    Rename refrence for key as .env    #
#                                       #
#########################################                                      


#Required Modules
1. Flask: The web framework used for building the application.
pip install Flask

2. SQLite: Used for local database management. No need to install separately if you have Python, as SQLite is part of Python’s standard library (sqlite3 module).

3. dotenv: To load environment variables from a .env file.
pip install python-dotenv

4. boto3: AWS SDK for Python, used for uploading/downloading the SQLite database to/from an S3 bucket.
pip install boto3

5. Pillow: For handling and manipulating images
pip install Pillow

6. PyAutoGUI: Used to capture screenshots in the screenshot_manager.py file.
pip install pyautogui

7. Timezone Management (Optional): If you're using timezone management, ensure the pytz module is installed.
pip install pytz



#Usage
Starting the Application
1. Run the Flask app:
python app.py

This will give a localhost link on terminal "127.0.0.1:5000" 

2. Access the application:
Go to 127.0.0.1:5000 for the main page with User and Admin options.

#User Functionality
1. User Signup and Login:
Users can sign up and log in from /signup and /login routes.
Once logged in, users can start and stop their day tracking.

2. Activity Tracking:
Mouse and keyboard activities are tracked when the user clicks the "Start Your Day" button.
The app captures periodic screenshots and stores the data in the SQLite database.

#Admin Functionality
1. Admin Signup and Login:
Admins can sign up and log in from /admin_signup and /admin_login routes.
2. Admin Dashboard:
The admin can view all users, and clicking on a user will show the activity log, including:
Active and inactive time.
Screenshots taken during their session.

#Syncing Database with AWS S3
Download Database: When the app starts, it downloads the most recent version of the database from S3 using s3_utils.py.
Upload Database: After every user signup, the local database is uploaded back to S3 to keep it in sync.

#Key Components
1. User Tracking
activity_tracker.py: Tracks mouse and keyboard activities.
screenshot_manager.py: Captures screenshots at set intervals and stores them in the screenshots folder.
2. Admin Dashboard
admin_dashboard.html: Displays users and their activity logs.
user_activity.html: Shows active/inactive times and screenshots for a selected user.

#Troubleshooting
1. Table Not Found:

Ensure the local_database.db is synced with S3.
Run the initialization script in s3_utils.py to create the necessary tables.

2. Screenshots Not Displaying:

Verify that the screenshots/ folder exists.
Check file paths when displaying screenshots in user_activity.html.

#Future Enhancements
Enhanced Reporting: Add graphs to visualize active vs inactive time per user.
Mobile Compatibility: Improve UI for mobile devices.
Role-Based Access: Implement more granular permissions for admins.

#Conclusion
This Employee Tracking Flask App provides a basic framework for tracking user activities with an admin review system. By using Flask, SQLite, and AWS S3, it ensures data persistence and ease of management for both users and administrators.


File Structutre

activity_tracker/
├── routes/
│   ├── admin.py   # Admin login/signup and dashboard routes
│   ├── auth.py    # User login/signup routes
│   ├── user.py    # User dashboard and activity routes
├── templates/
│   ├── admin_dashboard.html  # Admin dashboard
│   ├── dashboard.html        # User dashboard
│   ├── login.html            # User login page
│   ├── signup.html           # User signup page
│   ├── admin_login.html      # Admin login page
│   ├── admin_signup.html     # Admin signup page
│   └── user_activity.html    # Displays user activity and screenshots for admins
├── screenshots/              # Folder for storing captured screenshots
├── app.py                        # Main Flask application
├── .env                          # Environment variables (AWS credentials, etc.)
├── tracking/
│   ├── activity_tracker.py       # Tracks mouse and keyboard activity
│   ├── screenshot_manager.py     # Manages screenshot capturing
│   └── timezone_manager.py       # Handles timezone management
├── utils/
│   └── s3_utils.py               # Syncs database with AWS S3
└── local_database.db             # SQLite local database

