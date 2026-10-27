#!/usr/bin/env python3
"""
seed.py is going to be used to seed example data into the database for testing purposes. 
It is safe to rerun as it will reset all data from the database before seeding new data.
"""

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import datetime
with app.app_context():

	# reset data and add new example data, committing to db 
    print("Resetting database...")
    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()
    db.session.commit()

	#-----Exercise Data-----
    print("seeding exercise data...")
    treadmill = Exercise(name="Treadmill", category="Cardio", equipment_needed=True)
    jumping_jacks = Exercise(name="Jumping Jacks", category="Cardio", equipment_needed=False)
    jumping_rope = Exercise(name="Jumping Rope", category="Cardio", equipment_needed=True)
    push_ups = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
    cat_cow = Exercise(name="Cat-Cow Stretch", category="Flexibility", equipment_needed=False)
    yoga = Exercise(name="Yoga", category="Flexibility", equipment_needed=False)
    toe_touches = Exercise(name="Toe Touches", category="Flexibility", equipment_needed=False)
    burpees = Exercise(name="Burpees", category="HIIT", equipment_needed=False)
    mountain_climbers = Exercise(name="Mountain Climbers", category="HIIT", equipment_needed=False)
    jump_squats = Exercise(name="Jump Squats", category="HIIT", equipment_needed=False)
    
    db.session.add_all([treadmill, jumping_jacks, jumping_rope, push_ups, squats, bench_press, cat_cow, yoga, toe_touches, burpees, mountain_climbers, jump_squats])
    db.session.commit()

	#-----Workout Data-----
    print("seeding workout data...")
    workout1 = Workout(date=datetime(2026, 10, 27), duration_minutes=45, notes="Morning cardio session")
    workout2 = Workout(date=datetime(2026, 10, 28), duration_minutes=30, notes="Strength training with push-ups and squats")
    workout3 = Workout(date=datetime(2026, 10, 29), duration_minutes=60, notes="Flexibility and yoga session")
    workout4 = Workout(date=datetime(2026, 10, 30), duration_minutes=20, notes="High-intensity interval training (HIIT)")
    
    db.session.add_all([workout1, workout2, workout3, workout4])
    db.session.commit()

	#-----WorkoutExercise Data-----
    print("seeding workout exercise data...")
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=treadmill.id, sets=3, duration_seconds=600)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=jumping_jacks.id, sets=3, duration_seconds=300)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=push_ups.id, sets=4, reps=15)
    we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=squats.id, sets=4, reps=20)
    we5 = WorkoutExercise(workout_id=workout3.id, exercise_id=cat_cow.id, sets=2, duration_seconds=300)
    we6 = WorkoutExercise(workout_id=workout3.id, exercise_id=burpees.id, sets=3, duration_seconds=180)
    db.session.add_all([we1, we2, we3, we4, we5, we6])
    db.session.commit()

    print("Seeding complete!")