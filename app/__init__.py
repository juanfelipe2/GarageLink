from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

server = Server(host=app.config.get('HOST'), port=app.config.get('PORT'))
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', server)

from app.models import tables, forms
import app.controllers