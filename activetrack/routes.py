import json

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, flash, redirect, url_for, jsonify

from activetrack import app, db
from activetrack.models import User, Activity, Comment


@app.route("/")
def home():
    return render_template("home.html", user=current_user)


# Function to allow the user to log in to their account
@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        '''

        Error handling to check:
        - if password is correct
        - if username exists
        If no errors, user will be logged in.

        '''
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Successfully logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


# Function to allow the user to log out of their account
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Function to allow the user to sign up for an account
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    '''

    Error handling for form.
    If no errors, user details will be added to the database.

    '''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_name = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user_name:
            flash('Username already exists', category='error')
        elif user_email:
            flash('Email already exists', category='error')
        elif len(username) < 3:
            flash(
                'Username must be atleast 3 characters.',
                category='error')
        elif len(email) < 4:
            flash('Email is too short.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash(
                'Password is too short. Must be 7 plus characters.',
                category='error')
        else:
            try:
                # attempt to add new user to the database
                new_user = User(
                    username=username,
                    email=email,
                    password=generate_password_hash(
                        password1, method='sha256'
                    )
                )
                db.session.add(new_user)
                db.session.commit()
                flash('Successfully signed up! Please log in',
                      category='success')
                return redirect(url_for('login'))
            except Exception as e:
                # if an error occurs
                # cancel any potential changes made to the database
                db.session.rollback()
                # catch the error and flash a message
                flash(f'Error, failed to sign up: {str(e)}',
                      category='error')
    return render_template("sign_up.html", user=current_user)


@app.route('/diary')
@login_required
def diary():
    try:
        # attempt to load user activities
        user_activities = db.session.query(Activity).filter_by(
            user_id=current_user.id
        ).all()
        return render_template(
            "diary.html",
            user=current_user,
            activities=user_activities
        )
    except Exception as e:
        # catch the error and flash a message, redirect to home page
        flash(f'Error, failed to load activities: {str(e)}',
              category='error')
        return redirect(url_for('home'))


# Function to allow user to add an activity log
@app.route('/add_activity', methods=["GET", "POST"])
@login_required
def add_activity():
    if request.method == "POST":
        try:
            # attempt to add activity data to the database
            activity = Activity(
                user_id=current_user.id,
                workout_type=request.form.get("workout_type"),
                exercise_name=request.form.get("exercise_name"),
                reps=int(request.form.get(
                    "reps", 0)) if request.form.get("reps") else 0,
                distance=float(request.form.get(
                    "distance", 0)) if request.form.get("distance") else 0,
                sets=int(request.form.get(
                    "sets", 0)) if request.form.get("sets") else 0,
                weight=float(request.form.get(
                    "weight", 0)) if request.form.get("weight") else 0,
                duration=float(request.form.get(
                    "duration", 0)) if request.form.get("duration") else 0
            )
            db.session.add(activity)
            db.session.commit()
            flash('Activity added', category='success')
            return redirect(url_for('diary'))
        except Exception as e:
            # if an error occurs
            # cancel any potential changes made to the database
            db.session.rollback()
            # catch the error and flash a message
            flash(f'Error, failed to add an activity: {str(e)}',
                  category='error')

    return render_template("add_activity.html", user=current_user)


# Function to allow user to edit an activity log
@app.route('/edit_activity/<int:activity_id>', methods=["GET", "POST"])
@login_required
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)

    if activity.user_id != current_user.id:
        flash('You do not have permission to edit this activity.',
              category='error')
        return redirect(url_for('home'))

    if request.method == "POST":
        try:
            # attempt to update the database
            activity.workout_type = request.form.get("workout_type"),
            activity.exercise_name = request.form.get("exercise_name"),
            activity.reps = int(request.form.get(
                "reps", 0)) if request.form.get("reps") else 0,
            activity.distance = float(request.form.get(
                "distance", 0)) if request.form.get("distance") else 0,
            activity.sets = int(request.form.get(
                "sets", 0)) if request.form.get("sets") else 0,
            activity.weight = float(request.form.get(
                "weight", 0)) if request.form.get("weight") else 0,
            activity.duration = float(request.form.get(
                "duration", 0)) if request.form.get("duration") else 0
            db.session.commit()
            flash('Activity updated', category='success')
            return redirect(url_for('diary'))
        except Exception as e:
            # if an error occurs
            # cancel any potential changes made to the database
            db.session.rollback()
            # catch the error and flash a message
            flash(f'Error, failed to edit activity: {str(e)}',
                  category='error')

    return render_template(
        "edit_activity.html",
        user=current_user,
        activity=activity
    )


# Function to allow user to delete an activity log
@app.route('/delete_activity/<int:activity_id>')
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    try:
        # attempt to delete the activity from the database
        db.session.delete(activity)
        db.session.commit()
        flash('Activity deleted', category='success')
    except Exception as e:
        # if an error occurs
        # cancel any potential changes made to the database
        db.session.rollback()
        # catch the error and flash a message
        flash(f'Error, failed to delete activity: {str(e)}',
              category='error')

    return redirect(url_for('diary'))


# Function that loads the data from the json file
# passes into the exercises_data variable
@app.route('/get_exercises')
@login_required
def get_exercises():
    try:
        # attempt to open and load the json file
        with open("activetrack/data/exercises.json", "r") as json_data:
            exercises_data = json.load(json_data)
        return jsonify(exercises_data)
    except (IOError, json.JSONDecodeError) as e:
        # if there is an error loading the json file
        flash(f'Error, failed to load JSON file: {str(e)}',
              category='error')
        return redirect(url_for('diary'))
    except Exception as e:
        # if there is a general error
        flash(f'Error, failed to load exercises: {str(e)}',
              category='error')
        return redirect(url_for('diary'))


# Function to render all users activity logs on the activity feed page
@app.route('/activity_feed')
@login_required
def activity_feed():
    try:
        # attempt to load activity feed
        activities = list(Activity.query.order_by(Activity.created_at).all())
        return render_template(
            "activity_feed.html",
            user=current_user,
            activities=activities
        )
    except Exception as e:
        # catch the error and flash a message, redirect to home page
        flash(f'Error, failed to load activity feed: {str(e)}',
              category='error')
        return redirect(url_for('home'))


# Function to allow user to add a comment to an activity log
@app.route('/add_comment', methods=["GET", "POST"])
@login_required
def add_comment():
    if request.method == "POST":
        try:
            # attempt to add comment to the database
            comment = Comment(
                user_id=current_user.id,
                activity_id=request.form.get("activity_id"),
                comment_text=request.form.get("comment_text")
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added', category='success')
        except Exception as e:
            # if an error occurs
            # cancel any potential changes made to the database
            db.session.rollback()
            # catch the error and flash a message
            flash(f'Error, failed to add comment: {str(e)}',
                  category='error')
    return redirect(request.referrer or url_for('activity_feed'))


# Function to allow user to delete a comment
@app.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    try:
        # attempt to delete comment from database
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted', category='success')
    except Exception as e:
        # if an error occurs
        # cancel any potential changes made to the database
        db.session.rollback()
        # catch the error and flash a message
        flash(f'Error, failed to delete comment: {str(e)}',
              category='error')
    return redirect(request.referrer or url_for('activity_feed'))


"""
resource used for implementing errorhandler:
https://stackoverflow.com/questions/29516093/how-to-redirect-to-a-external-404-page-python-flask

error handlers direct to error.html with error_message variable passed
each error_message variable holds a string value relevant to the error
"""


@app.errorhandler(400)
def error_400(e):
    error_message = "The server cannot process the request."
    return render_template(
        "error.html",
        user=current_user,
        error_message=error_message
    ), 400


@app.errorhandler(401)
def error_401(e):
    error_message = "You are not authorized to view that page."
    return render_template(
        "error.html",
        user=current_user,
        error_message=error_message
    ), 401


@app.errorhandler(403)
def error_403(e):
    error_message = "You do not have permission to view that page."
    return render_template(
        "error.html",
        user=current_user,
        error_message=error_message
    ), 403


@app.errorhandler(404)
def error_404(e):
    error_message = "Page not found."
    return render_template(
        "error.html",
        user=current_user,
        error_message=error_message
    ), 404


@app.errorhandler(500)
def error_500(e):
    error_message = "Internal server error."
    return render_template(
        "error.html",
        user=current_user,
        error_message=error_message
    ), 500
