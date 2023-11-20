from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdsfdsfds'
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'centras.db')
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

db = SQLAlchemy(app)
manager = LoginManager(app)
admin = Admin(app)

from project_app import views, admin_views, models

admin.add_view(ModelView(models.Gyventojas, db.session))
admin.add_view(ModelView(models.Salys, db.session))
admin.add_view(ModelView(models.Sklaida, db.session))
