from flask import render_template
from activetrack import app, db
from activetrack.models import User, Exercise, Activity, Comment


@app.route("/")
def home():
    return render_template("base.html")