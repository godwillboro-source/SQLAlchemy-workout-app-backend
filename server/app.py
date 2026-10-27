from flask import Flask, make_response
from flask_migrate import Migrate


from models import db, Exercise, Workout, WorkoutExercise
from models import exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route("/")
def home():
    return make_response("<h1>Welcome to the Workout App API!</h1>", 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

