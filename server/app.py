from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from models import exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

#--------Validation Functions--------

def validate_exercise_data(data):
    errors = {}
    
    # Only validate name if it was provided
    if "name" in data:
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            errors["name"] = ["Exercise name cannot be empty."]
        else:
            data["name"] = name.strip()

    # Only validate category if it was provided (crucial for PATCH requests!)
    if "category" in data:
        category = data.get("category")
        valid_categories = {"Cardio", "Strength", "Flexibility", "HIIT"}
        if category not in valid_categories:
            errors["category"] = [
                "Category must be one of Cardio, Strength, Flexibility, or HIIT."
            ]

    return errors

def validate_workout_data(data):
    errors = {}
    
    # Only validate date if it was provided
    if "date" in data:
        if not data.get("date"):
            errors["date"] = ["Workout date cannot be empty."]

    # Only validate duration_minutes if it was provided
    if "duration_minutes" in data:
        duration = data.get("duration_minutes")
        if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
            errors["duration_minutes"] = ["Workout duration must be greater than 0."]

    # Only validate notes if it was provided
    if "notes" in data:
        notes = data.get("notes")
        if notes is not None and len(notes) > 255:
            errors["notes"] = ["Notes cannot exceed 255 characters."]

    return errors

def validate_workout_exercise_data(data):
    errors = {}
    
    for field in ("sets", "reps", "duration_seconds"):
        # Only validate the field if it was actually included in the request
        if field in data:
            value = data.get(field)
            if value is None:
                continue
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                label = field.replace("_", " ").capitalize()
                errors[field] = [f"{label} must be greater than 0."]

    return errors


# Define Routes here
@app.route("/")
def home():
    return make_response("<h1>Welcome to the Workout App API!</h1>", 200)

#--------Exercise Routes--------

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)

@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise:
        return make_response(exercise_schema.dump(exercise), 200)
    else:
        return make_response({"error": "Exercise not found"}, 404)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    if not data:
        return make_response({"error": "No input data provided"}, 400)
    try:
        exercise_data = exercise_schema.load(data)
        errors = validate_exercise_data(exercise_data)
        if errors:
            return make_response({"errors": errors}, 400)

        new_exercise = Exercise(**exercise_data)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(new_exercise), 201)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        return make_response({"message": "Exercise deleted successfully"}, 200)
    else:
        return make_response({"error": "Exercise not found"}, 404)

@app.route("/exercises/<int:id>", methods=["PATCH"])
def update_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    data = request.get_json()
    if not data:
        return make_response({"error": "No input data provided"}, 400)

    try:
        exercise_data = exercise_schema.load(data, partial=True)
        errors = validate_exercise_data(exercise_data)
        if errors:
            return make_response({"errors": errors}, 400)

        for key, value in exercise_data.items():
            setattr(exercise, key, value)

        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 200)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)


#--------Workout Routes--------
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get(id)
    if workout:
        return make_response(workout_schema.dump(workout), 200)
    else:
        return make_response({"error": "Workout not found"}, 404)

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    if not data:
        return make_response({"error": "No input data provided"}, 400)
    try:
        workout_data = workout_schema.load(data)
        errors = validate_workout_data(workout_data)
        if errors:
            return make_response({"errors": errors}, 400)

        new_workout = Workout(**workout_data)
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.dump(new_workout), 201)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)

@app.route("/workouts/<int:id>", methods=["PATCH"])
def update_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    data = request.get_json()
    if not data:
        return make_response({"error": "No input data provided"}, 400)

    try:
        workout_data = workout_schema.load(data, partial=True)
        errors = validate_workout_data(workout_data)
        if errors:
            return make_response({"errors": errors}, 400)

        for key, value in workout_data.items():
            setattr(workout, key, value)

        db.session.commit()
        return make_response(workout_schema.dump(workout), 200)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if workout:
        db.session.delete(workout)
        db.session.commit()
        return make_response({"message": "Workout deleted successfully"}, 200)
    else:
        return make_response({"error": "Workout not found"}, 404)


#--------WorkoutExercise Routes--------
@app.route("/workout_exercises", methods=["GET"])
def get_workout_exercises():
    workout_exercises = WorkoutExercise.query.all()
    return make_response(workout_exercise_schema.dump(workout_exercises, many=True), 200)

@app.route("/workout_exercises/<int:id>", methods=["GET"])
def get_workout_exercise(id):
    workout_exercise = WorkoutExercise.query.get(id)
    if workout_exercise:
        return make_response(workout_exercise_schema.dump(workout_exercise), 200)
    else:
        return make_response({"error": "WorkoutExercise not found"}, 404)

from sqlalchemy.exc import IntegrityError

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    data = request.get_json() or {}
    # IDs come from the URL, so they override anything in the body
    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    try:
        we_data = workout_exercise_schema.load(data)
        errors = validate_workout_exercise_data(we_data)
        if errors:
            return make_response({"errors": errors}, 400)

        new_we = WorkoutExercise(**we_data)
        db.session.add(new_we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_we), 201)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)
    except IntegrityError:
        db.session.rollback()
        return make_response({"error": "Could not create workout exercise"}, 400)

@app.route("/workout_exercises/<int:id>", methods=["PATCH"])
def update_workout_exercise(id):
    workout_exercise = WorkoutExercise.query.get(id)
    if not workout_exercise:
        return make_response({"error": "WorkoutExercise not found"}, 404)

    data = request.get_json()
    if not data:
        return make_response({"error": "No input data provided"}, 400)

    try:
        workout_exercise_data = workout_exercise_schema.load(data, partial=True)
        errors = validate_workout_exercise_data(workout_exercise_data)
        if errors:
            return make_response({"errors": errors}, 400)

        for key, value in workout_exercise_data.items():
            setattr(workout_exercise, key, value)

        db.session.commit()
        return make_response(workout_exercise_schema.dump(workout_exercise), 200)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)

@app.route("/workout_exercises/<int:id>", methods=["DELETE"])
def delete_workout_exercise(id):
    workout_exercise = WorkoutExercise.query.get(id)
    if workout_exercise:
        db.session.delete(workout_exercise)
        db.session.commit()
        return make_response({"message": "WorkoutExercise deleted successfully"}, 200)
    else:
        return make_response({"error": "WorkoutExercise not found"}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
