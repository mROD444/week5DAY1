from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)
moment = Moment(app)

login_manager.login_view = 'login'
login_manager.login_message = 'You must log in to view this page'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)