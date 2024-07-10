from flask import render_template, request, flash, redirect, url_for
from activetrack import app, db
from activetrack.models import User, Exercise, Activity, Comment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


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
                return redirect(url_for('diary'))
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
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up! Please log in', category='success')
            return redirect(url_for('login'))

    return render_template("sign_up.html", user=current_user)


@app.route('/diary')
@login_required
def diary():
    activities = list(Activity.query.order_by(Activity.created_at).all())
    #user_activities = db.session.query(Activity).filter_by(user_id=current_user.id).all()
    return render_template("diary.html", user=current_user, activities=activities)


# Function to allow user to add an activity log
@app.route('/add_activity', methods=["GET", "POST"])
@login_required
def add_activity():
    if request.method == "POST":
        activity = Activity(
            user_id=current_user.id,
            workout_type=request.form.get("workout_type"),
            exercise_name=request.form.get("exercise_name"),
            reps=int(request.form.get("reps", 0)) if request.form.get("reps") else 0,
            distance=float(request.form.get("distance", 0)) if request.form.get("distance") else 0,
            sets=int(request.form.get("sets", 0)) if request.form.get("sets") else 0,
            weight=float(request.form.get("weight", 0)) if request.form.get("weight") else 0,
            duration=float(request.form.get("duration", 0)) if request.form.get("duration") else 0
        )
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('diary'))

    return render_template("add_activity.html", user=current_user)


# Function to allow user to edit an activity log
@app.route('/edit_activity/<int:activity_id>', methods=["GET", "POST"])
@login_required
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if request.method == "POST":
        activity.workout_type=request.form.get("workout_type"),
        activity.exercise_name=request.form.get("exercise_name"),
        activity.reps=int(request.form.get("reps", 0)) if request.form.get("reps") else 0,
        activity.distance=float(request.form.get("distance", 0)) if request.form.get("distance") else 0,
        activity.sets=int(request.form.get("sets", 0)) if request.form.get("sets") else 0,
        activity.weight=float(request.form.get("weight", 0)) if request.form.get("weight") else 0,
        activity.duration=float(request.form.get("duration", 0)) if request.form.get("duration") else 0
        db.session.commit()
        return redirect(url_for('diary'))

    return render_template("edit_activity.html", user=current_user, activity=activity)


# Function to allow user to delete an activity log
@app.route('/delete_activity/<int:activity_id>')
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    return redirect(url_for('diary'))