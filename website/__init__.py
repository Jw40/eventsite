#import flask - from the package import class
from re import template
from flask import Flask
from flask.templating import render_template 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
   app=Flask(__name__)  # this is the name of the module/package that is calling this app
   app.debug=True
   app.secret_key='utroutoru'

   #config upload folder
   UPLOAD_FOLDER = '/static/image'
   app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

   uri = os.getenv("DATABASE_URL")  # or other relevant config var
   if uri and uri.startswith("postgres://"):
      uri = uri.replace("postgres://", "postgresql://", 1)
   #set the app configuration data 

   #Postgres Database uncomment if you wish to use this.
   #app.config['SQLALCHEMY_DATABASE_URI']= uri

   #Sqlite Database uncomment if you wish to use this.
   app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///sitedata.sqlite'

   #initialize db with flask app
   db.init_app(app)

   bootstrap = Bootstrap(app)
    
   #initialize the login manager
   login_manager = LoginManager()
    
   #set the name of the login function that lets user login
   # in our case it is auth.login (blueprintname.viewfunction name)
   login_manager.login_view='auth.login'
   login_manager.init_app(app)

   #create a user loader function takes userid and returns User
   from .models import User  # importing here to avoid circular references
   @login_manager.user_loader
   def load_user(user_id):
      return User.query.get(int(user_id))

   #importing views module here to avoid circular references
   # a commonly used practice.
   from . import views
   app.register_blueprint(views.mainbp)

   #needs setting up
   from . import events
   app.register_blueprint(events.bp)

   from . import auth
   app.register_blueprint(auth.bp)
   
   @app.errorhandler(404)
   def page_not_found(e):
      return render_template('error/404.html'),404
   
   @app.errorhandler(500)
   def internal_server_error(e):
      return render_template('error/505.html'),500
   return app



