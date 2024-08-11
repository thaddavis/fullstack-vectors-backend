from fastapi import APIRouter, Query as FastAPIQuery
from pydantic import BaseModel
from src.db.models import Workout
from src.deps import db_dependency, user_dependency

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/workouts")
def workouts(db: db_dependency, user: user_dependency, query: Query, cursor: int | bool = FastAPIQuery(...)):

    print('query.query', query.query)

    workouts = db.query(Workout).offset(cursor).limit(8).all()
    cursor += 8

    return { 
        'data': workouts,
        'cursor': cursor
    }