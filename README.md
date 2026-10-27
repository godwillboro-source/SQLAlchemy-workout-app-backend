# Workout Tracker API

## Description

A RESTful backend API for a workout tracking application used by personal trainers. Built with Flask, SQLAlchemy, and Marshmallow, it allows trainers to manage reusable exercises, create dated workout sessions, and associate exercises with workouts while storing per-exercise performance data such as sets, reps, and duration.

The API enforces data integrity at three layers: database table constraints, SQLAlchemy model validations, and Marshmallow schema validations.

Each Table has its own CRUD functions. All tables have a GET, POST PATCH AND DELETE

## Installation

### Prerequisites
- Python 3.8.13

### Steps

```bash
git clone https://github.com/godwillboro-source/SQLAlchemy-workout-app-backend.git
cd SQLAlchemy-workout-app-backend
```
- Initiate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```
- Once activated, install the dependencies from requirements.txt

```bash
pip install -r requirements.txt
```

## Running the App

```bash
cd server
```
- Seed sample Data by running the seed file

```bash
python3 seed.py
```
Activate the API by running the app file

```bash
python3 app.py
```

The API will be available at http://localhost:5555.

## Endpoints

### Exercise Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /exercises | List all exercises |
| GET | /exercises/\<id> | Get a single exercise with its associated workouts |
| POST | /exercises | Create a new exercise |
| DELETE | /exercises/\<id> | Delete an exercise |
| PATCH | /exercises/\<id> | Update an existing workout |

### Workout Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /workouts | List all workouts |
| GET | /workouts/\<id> | Get a single workout with its exercises and sets, reps/duration |
| POST | /workouts | Create a new workout |
| DELETE | /workouts/\<id> | Delete a workout |
| PATCH | /workouts/\<id> | Update an existing workout |

### Workout_Exercises Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /workout_exercises | List all exercises recorded across workouts |
| GET | /workout_exercises/\<id> | retrieves one exercise entry from a workout using its ID |
| POST | /workouts/\<id>/exercises/\<id>/workout_exercises | creates a workout-exercise entry, linking an exercise to an existing workout |
| DELETE | /workout_exercises/\<id> | Delete a workout-exercise entry |
| PATCH | /workout_exercises/\<id> | Update an existing workout-exercise entry |

