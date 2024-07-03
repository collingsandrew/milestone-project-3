from flask import render_template, request, flash
from activetrack import app, db
from activetrack.models import User, Exercise, Activity, Comment


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    return "<p>Logout</p>"


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 3:
            flash('Username must be atleast 3 characters.',
            category='error')
        elif len(email) < 4:
            flash('Email is too short.',
            category='error')
        elif password1 != password2:
            flash('Passwords do not match.',
            category='error')
        elif len(password1) < 7:
            flash('Password is too short, please enter more than 7 characters.',
            category='error')
        else:
            flash('Signed up!', category='success')

    return render_template("sign_up.html")