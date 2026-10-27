from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy import CheckConstraint
db = SQLAlchemy()



"""Our models and schemas will be defined in this file, each model with its corressponding schema. Models represent the table structures while schemas 
handle the serialization and deserialization of data.
"""
# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'
    __table_args__ = (
        CheckConstraint(
            "category IN ('Cardio', 'Strength', 'Flexibility', 'HIIT')",
            name='ck_exercises_valid_category',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    #Exercise name should be unique and not null
    name = db.Column(db.String(100), nullable=False, unique=True)

    #Exercise category should be not null and can be one of the following: 'Cardio', 'Strength', 'Flexibility', 'HIIT'
    category = db.Column(db.String(50), nullable=False)

    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean(default=False)
    workout_exercises = fields.List(fields.Nested('WorkoutExerciseSchema', exclude=('exercise',)))

class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = (
        CheckConstraint(
            'duration_minutes > 0',
            name='ck_workouts_positive_duration',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    #Workout duration in minutes should be not null and greater than 0
    duration_minutes = db.Column(db.Integer, nullable=False)

    notes = db.Column(db.String(255), nullable=True)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True)
    notes = fields.String()
    workout_exercises = fields.List(fields.Nested('WorkoutExerciseSchema', exclude=('workout',)))

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    __table_args__ = (
        CheckConstraint('sets > 0', name='ck_workout_exercises_positive_sets'),
        CheckConstraint(
            'reps IS NULL OR reps > 0',
            name='ck_workout_exercises_positive_reps',
        ),
    )

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

class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    sets = fields.Integer(required=True)
    reps = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    workout = fields.Nested(lambda: WorkoutSchema, exclude=('workout_exercises',))
    exercise = fields.Nested(lambda: ExerciseSchema, exclude=('workout_exercises',))


exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()

exercises_schema = ExerciseSchema(many=True, exclude=('workout_exercises',))
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
workout_exercises_schema = WorkoutExerciseSchema(many=True, exclude=('workout', 'exercise'))