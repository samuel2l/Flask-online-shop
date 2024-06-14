from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = ''#add app secret key
app.config['SQLALCHEMY_DATABASE_URI'] = #add db URI
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#line below tells login_manager where the login page is
login_manager.login_view='login_page'
login_manager.login_message_category='info'
from store import routes
