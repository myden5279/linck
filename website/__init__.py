from flask import Flask
import os
from werkzeug.utils import secure_filename  # The name of the file may be harmful so we use this function to
# to rename it
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy is used to create daatabase for our webapp
from flask_login import LoginManager


DB_NAME = "users.db"  # This is going to be the name of our database

db = SQLAlchemy()  # We are just initializing the database


def create_app():
    App = Flask(__name__)
    # config contains a set of variable which can be modified as per our need
    App.config["SECRET_KEY"] = "hello this is the first website"  # this is a secret key to encrypt the content
    App.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # this is gonna be the path for
    # our database

    db.init_app(App)  # While creating the object of the SQLAlchemy() we have to give out app variable
    # but in our case it is not possible so we use the init_app() method to set the correct config

    from .views import route
    from .auth import auth

    App.register_blueprint(route, url_prefix="/")  # we are initializing the path of the sites by creating the blueprint in
    App.register_blueprint(auth, url_prefix='/')  # other files

    # the following if statement checks if database is already in the tmp folder
    # this is gonna run only one time
    from .models import Posts, Users

    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=App)
        print('database created successfully')

    loginmanager = LoginManager()
    loginmanager.login_view = 'auth.sign_in'
    loginmanager.init_app(App)

    @loginmanager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return App
