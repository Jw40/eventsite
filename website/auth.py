#authentication for logon to the web application

from flask import (Blueprint, flash, render_template, request, url_for, redirect) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user, current_user
from . import db

#create a blueprint
bp = Blueprint('auth', __name__)

#login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        #get the username and password from the database
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        #if there is no user with that name
        if u1 is None:
            error='Incorrect user name, Please try again.'
        #check the password - notice password hash function
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password, Please try again.'
        if error is None:
            #all good, set the login_user of flask_login to manage the user
            login_user(u1)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error, 'login_error')
    return render_template('user.html', form=login_form, heading='Login')



#register
@bp.route('/register', methods=['GET','POST'])
def register():
    register = RegisterForm()
    if register.validate_on_submit():
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        message = 'Registered Successfully'
        # Check if the user name already exists
        u1 = User.query.filter_by(name=uname).first()
        if u1:
            flash('User name already exists. Please login.', 'register_error')
            return redirect(url_for('auth.login'))
        email1 = User.query.filter_by(emailid = email).first()
        if email1:
            flash('This email address has been registered. Please try again.', 'register_error')
            return redirect(url_for('auth.login'))
        
        # Generate a password hash to store and commit the new user to the database
        pwd_hash = generate_password_hash(pwd)
        new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        flash(message, 'register_error')
        return redirect(url_for('auth.login'))

    else:    
        return render_template('user.html', form=register, heading='Register')

#logout
@bp.route("/logout", methods=['GET','POST'])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.index'))
