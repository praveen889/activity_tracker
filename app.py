from flask import Flask
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') 


# Register blueprints for modular routes
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)
