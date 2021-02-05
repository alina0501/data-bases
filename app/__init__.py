from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os


def del_last_child(the_url):
    the_arr = the_url.split('/')
    the_arr.pop()
    return '/'.join(the_arr)


app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
os.makedirs(os.path.join(del_last_child(app.instance_path), 'app/static/instance/img'), exist_ok=True)
from app import routes, models
