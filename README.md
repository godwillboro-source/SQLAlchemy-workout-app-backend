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

# Endpoints