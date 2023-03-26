# All of the imports that are needed for this page to operate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_session import Session
# Certifi allows MongoDB files to work and opperate smoothly
import certifi
# Our database connection and how it is set up for the authentication later 
ca = certifi.where()
client = MongoClient("mongodb+srv://mrmutturaja389:FBLA202223@fbla.mrh4gqm.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.dpfbla
s = db.fbladata
c = db.clubs
def create_app():
    # Sets up app for the program to run
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    # sets up flask login in application
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_json = s.find_one({'_id': ObjectId(user_id)})
        return User(user_json)

    return app