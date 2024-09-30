import boto3
import sqlite3
import os
from dotenv import load_dotenv


def get_db_connection():
    conn = sqlite3.connect('local_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            mouse_activity TEXT,
            keyboard_activity TEXT,
            screenshot_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call this function once to initialize the database
init_db()

# Load environment variables from .env file
load_dotenv()

# Amazon S3 configuration
S3_BUCKET = os.getenv('S3_BUCKET', 'main-bucket')
S3_DB_KEY = os.getenv('S3_DB_KEY', 'main_database.db')
LOCAL_DB_PATH = os.getenv('LOCAL_DB_PATH', 'local_database.db')

# Initialize S3 client using environment variables
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# Download the SQLite database from S3
def download_db_from_s3():
    try:
        print(f"Attempting to download the database from S3 bucket: {S3_BUCKET}, key: {S3_DB_KEY}")
        s3_object = s3.get_object(Bucket=S3_BUCKET, Key=S3_DB_KEY)
        with open(LOCAL_DB_PATH, 'wb') as f:
            f.write(s3_object['Body'].read())
        print("Database downloaded from S3.")
    except Exception as e:
        print(f"Error downloading the database from S3: {e}")
        # Handle cases where the database does not exist in S3
        if 'NoSuchKey' in str(e):
            print(f"Database not found in S3 at key: {S3_DB_KEY}. A new database will be created locally.")
        else:
            raise e

# Upload the SQLite database to S3
def upload_db_to_s3():
    try:
        print(f"Uploading database to S3 bucket: {S3_BUCKET}, key: {S3_DB_KEY}")
        with open(LOCAL_DB_PATH, 'rb') as f:
            s3.upload_fileobj(f, S3_BUCKET, S3_DB_KEY)
        print("Database uploaded to S3.")
    except Exception as e:
        print(f"Error uploading the database to S3: {e}")

# Establish a connection to the local SQLite database
def get_db_connection():
    # Ensure the local database is the latest version from S3
    download_db_from_s3()

    # Create a connection to the local SQLite database
    conn = sqlite3.connect(LOCAL_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
