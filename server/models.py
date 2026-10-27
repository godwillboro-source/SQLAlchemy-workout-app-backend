from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate, validates
from datetime import datetime
db = SQLAlchemy()



"""Our models and schemas will be defined in this file, each model with its corressponding schema. Models represent the table structures while schemas 
handle the serialization and deserialization of data.
"""
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
        if not name or name.strip() == "":
            raise ValueError("Exercise name cannot be empty.")
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Cardio', 'Strength', 'Flexibility', 'HIIT']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}.")
        return category

class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, error="Exercise name cannot be empty."))
    category = fields.String(required=True, validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'HIIT'], error="Category must be one of 'Cardio', 'Strength', 'Flexibility', 'HIIT'."))
    equipment_needed = fields.Boolean(default=False)

    workout_exercises = fields.List(fields.Nested('WorkoutExerciseSchema', exclude=('exercise',)))

    @validates('name')
    def validate_name(self, name):
        if not name or name.strip() == "":
            raise ValueError("Exercise name cannot be empty.")
        return name.strip()

    @validates('category')
    def validate_category(self, category):
        valid_categories = ['Cardio', 'Strength', 'Flexibility', 'HIIT']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}.")
        return category
    
class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Range(min=1, error="Exercise name cannot be empty."))
    category = fields.String(required=True, validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'HIIT'], error="Category must be one of 'Cardio', 'Strength', 'Flexibility', 'HIIT'."))
    equipment_needed = fields.Boolean(default=False)

    workout_exercises = fields.List(fields.Nested('WorkoutExerciseSchema', exclude=('exercise',)))

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

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True, error_messages={"required": "Workout date cannot be empty."})
    duration_minutes = fields.Integer(required=True, validate=validate.Length(min=1, error="Workout duration must be greater than 0."))
    notes = fields.String(validate=validate.Length(max=255))

    workout_exercises = fields.List(fields.Nested('WorkoutExerciseSchema', exclude=('workout',)))

    @validates('duration_minutes')
    def validate_duration_minutes(self, duration):
        if duration <= 0:
            raise ValueError("Workout duration must be greater than 0.")
        return duration
    
    @validates('date')
    def validate_date(self, date):
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
    reps = db.Column(db.Integer, nullable=True)

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
        if reps is not None and reps <= 0:
            raise ValueError("Reps must be greater than 0.")
        return reps

class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    sets = fields.Integer(required=True, validate=validate.Range(min=1, error="Sets must be greater than 0."))
    reps = fields.Integer(required=True, validate=validate.Range(min=1, error="Reps must be greater than 0."))
    duration_seconds = fields.Integer(validate=validate.Range(min=1, error="Duration seconds must be greater than 0."))

    workout = fields.Nested(lambda: WorkoutSchema, exclude=('workout_exercises',))
    exercise = fields.Nested(lambda: ExerciseSchema, exclude=('workout_exercises',))

    @validates('sets')
    def validate_sets(self, sets):
        if sets <= 0:
            raise ValueError("Sets must be greater than 0.")
        return sets

    @validates('reps')
    def validate_reps(self, reps):
        if reps is not None and reps <= 0:
            raise ValueError("Reps must be greater than 0.")
        return reps

    #since duration is nullable, we only validate if the value is provided.
    @validates('duration_seconds')
    def validate_duration_seconds(self, seconds):
        if seconds is not None and seconds <= 0:
            raise ValueError("Duration seconds must be greater than 0.")
        return seconds


exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()

exercises_schema = ExerciseSchema(many=True, exclude=('workout_exercises',))
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
workout_exercises_schema = WorkoutExerciseSchema(many=True, exclude=('workout', 'exercise'))