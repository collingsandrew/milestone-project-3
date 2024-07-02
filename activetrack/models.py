from activetrack import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func


# Relationships added to classes with ondelete="CASCADE" set on releveant classes
# When one data entry is removed, the data relating to that in another table is also deleted

class User(db.Model, UserMixin):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    activities = db.relationship('Activity', backref='user', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"#{self.id}|username:{self.username}| email:{self.email}"

class Exercise(db.Model):
    # schema for the Exercise model
    id = db.Column(db.Integer, primary_key=True)
    exercise_type = db.Column(db.String(250), nullable=False)
    exercise_name = db.Column(db.String(250), nullable=False)
    activities = db.relationship('Activity', backref='exercise', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"#{self.id}|exercise_type:{self.exercise_type}|exercise_name:{self.exercise_name}"

class Activity(db.Model):
    # schema for the Activity model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete="CASCADE"), nullable=False)
    exercise_name = db.Column(db.String, nullable=False)
    reps = db.Column(db.Integer)
    distance = db.Column(db.Numeric)
    sets = db.Column(db.Integer)
    duration = db.Column(db.Numeric)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment', backref='activity', lazy=True, cascade="all, delete")

    def __repr__(self):
        return (f"<Activity id={self.id}|exercise_name={self.exercise_name}|reps={self.reps}|distance={self.distance}"
                f"sets={self.sets}|duration={self.duration}|created_at={self.created_at}>")

class Comment(db.Model):
    # schema for the Comment model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete="CASCADE"), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"#{self.id}|comment_text:{self.comment_text}|created_at:{self.created_at}"