from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd62d76093d27346969cea3341e1e1d27'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_maneger = LoginManager(app)
login_maneger.login_view = 'login'
login_maneger.login_message = u'Realize o login ou Registre-se para Acessar.'
login_maneger.login_message_category = 'alert-info'

from fourteen import routes