from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status

from src.db.models import Workout
from src.deps import db_dependency, jwt_dependency

router = APIRouter()

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class WorkoutCreate(WorkoutBase):
    pass


@router.get('/')
def get_workout(db: db_dependency, jwt: jwt_dependency, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()

@router.get('/workouts')
def get_workouts(db: db_dependency, jwt: jwt_dependency):
    return db.query(Workout).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_workout(db: db_dependency, jwt: jwt_dependency, workout: WorkoutCreate):
    db_workout = Workout(**workout.model_dump(), user_id=jwt.get('id'))
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.delete("/")
def delete_workout(db: db_dependency, jwt: jwt_dependency, workout_id: int):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout:
        db.delete(db_workout)
        db.commit()
    return db_workout