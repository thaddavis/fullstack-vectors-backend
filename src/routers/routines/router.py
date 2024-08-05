from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from src.db.models import Workout, Routine
from src.deps import db_dependency, user_dependency

router = APIRouter()

class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class RoutineCreate(RoutineBase):
    workouts: List[int] = []
    
@router.get("/")
def get_routines(db: db_dependency, user: user_dependency):
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == user.get('id')).all()

@router.post("/")
def create_routine(db: db_dependency, user: user_dependency, routine: RoutineCreate):
    db_routine = Routine(name=routine.name, description=routine.description, user_id=user.get('id'))
    for workout_id in routine.workouts:
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            db_routine.workouts.append(workout)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    db_routines = db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.id == db_routine.id).first()
    return db_routines

@router.delete('/')
def delete_routine(db: db_dependency, user: user_dependency, routine_id: int):
    db_routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if db_routine:
        db.delete(db_routine)
        db.commit()
    return db_routine