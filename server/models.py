from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)

    #Exercise name should be unique and not null
    name = db.Column(db.String(100), nullable=False, unique=True)

    #Exercise category should be not null and can be one of the following: 'Cardio', 'Strength', 'Flexibility', 'HIIT'
    category = db.Column(db.String(50), nullable=False)

    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip():
            raise ValueError("Exercise name cannot be empty.")
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Cardio', 'Strength', 'Flexibility', 'HIIT']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}.")
        return category

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    #Workout duration in minutes should be not null and greater than 0
    duration_minutes = db.Column(db.Integer, nullable=False)

    notes = db.Column(db.String(255), nullable=True)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise ValueError("Workout duration must be greater than 0.")
        return duration

    @validates('date')
    def validate_date(self, key, date):
        if not date:
            raise ValueError("Workout date cannot be empty.")
        return date
    
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    #Workout exercise sets should be not null and greater than 0
    sets = db.Column(db.Integer, nullable=False)

    #Workout exercise reps should be not null and greater than 0
    reps = db.Column(db.Integer, nullable=False)

    duration_seconds = db.Column(db.Integer, nullable=True)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets <= 0:
            raise ValueError("Sets must be greater than 0.")
        return sets
    @validates('reps')
    def validate_reps(self, key, reps):
        if reps <= 0:
            raise ValueError("Reps must be greater than 0.")
        return reps