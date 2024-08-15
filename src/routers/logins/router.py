from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status

from src.db.models import Logins
from src.deps import db_dependency, jwt_dependency

router = APIRouter()

@router.get('/')
def get_logins(db: db_dependency, jwt: jwt_dependency):
    print("---> get_workouts <---")
    print('jwt', jwt)
    return db.query(Logins).filter(Logins.account_id == jwt.get('id')).order_by(Logins.created_at.desc()).all()
    
# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_workout(db: db_dependency, jwt: jwt_dependency, workout: WorkoutCreate):
#     db_workout = Workout(**workout.model_dump(), user_id=user.get('id'))
#     db.add(db_workout)
#     db.commit()
#     db.refresh(db_workout)
#     return db_workout