from flask import Flask, request, redirect, url_for, render_template, flash,session
from flask import Blueprint
from models import register,verify_user
forms_app= Blueprint('forms_app', __name__)

@forms_app.route('/register', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cpassword= request.form['cpassword']
        email= request.form['email']
        age = request.form['age']
        gender= request.form['gender']
        mobile = request.form['mobile']
        country= request.form['country']
        state = request.form['state']

    if not register(username,password,email,age,gender,mobile,country,state):
       flash('A user with that username already exists.')
       return redirect(request.referrer)
    else:
        flash("User Account created successfully")
        return redirect(request.referrer)



@forms_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not verify_user(username,password):
            flash('Incorrect Username or Password !')
        else:
            session['username'] = username
            flash('Logged in successfully!')
            return redirect(url_for('main'))

        return redirect(request.referrer)

