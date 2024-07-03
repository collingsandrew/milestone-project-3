from flask import render_template
from activetrack import app, db
from activetrack.models import User, Exercise, Activity, Comment


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return "<p>Login</p>"


@app.route('/logout')
def logout():
    return "<p>Logout</p>"


@app.route('/sign-up')
def sign_up():
    return "<p>Sign Up</p>"