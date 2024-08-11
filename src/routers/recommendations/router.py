from fastapi import APIRouter, Response, Query as FastAPIQuery
from pydantic import BaseModel

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/workouts")
def workouts(query: Query, cursor: int = FastAPIQuery(...)):
    
    print('---> query <---', query, cursor)

    # response.status_code = 200
    return {"status": "OK!"}