from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///radiologyassistant.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from radiology_assistant.utils import dump_temp
with app.app_context():
    dump_temp()
from radiology_assistant import routes