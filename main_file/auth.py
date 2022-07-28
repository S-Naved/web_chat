from flask import Blueprint, redirect, render_template,session,flash,request,url_for
from flask_login import logout_user,login_user,login_required
from werkzeug.security import ( generate_password_hash,
                               check_password_hash )
from datetime import datetime
from . import db
from .model import User
import os
auth = Blueprint('auth',__name__)

@auth.route('/login' , methods = ['GET' , 'POST'])
def login():
    if request.method == 'POST':
        email   = request.form.get('email')
        password= request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
               login_user(user)
               session.permanent = True
               return redirect(url_for('views.home'))
            else:
                flash ('Invalid Passowrd',category = 'error')
                return redirect(url_for('auth.login'))
        else:
                flash ('Invalid Email',category = 'error')
                return redirect(url_for('auth.login'))
    return render_template('login.html')
    
@auth.route('/register', methods = ['GET','POST'])
def register():
    if request.method =='POST':
        username    = request.form.get('username')
        email       = request.form.get('email')
        password1   = request.form.get('password1')
        password2   = request.form.get('password2')
        email_exist = User.query.filter_by(email=email).first()  

        if email_exist:
            flash('Email is already in use',category = 'error')
        elif password1 != password2:
            flash('Password don\'t match',  category = 'error')  
        elif len(username)< 3:
            flash('Username is too short.', category = 'error')
        elif len(password1)< 4:
            flash('Password is too short.', category = 'error')
        else:
            date_created=  datetime.now()
            date_create =  datetime.utcnow()
            new_user = User(email = email,username = username, 
                            password = generate_password_hash
                            (password1,method = 'sha256'),
                            date_created = date_created,
                            date_create = date_create)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember = True)
            
            return redirect(url_for('views.home'))
    return render_template ('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successfully !',category = 'success')
    return redirect(url_for('auth.login'))

