from fastapi import APIRouter, Query as FastAPIQuery
from pydantic import BaseModel
from src.db.models import Workout
from src.deps import db_dependency, user_dependency
from core.clients import pc
import os
import requests

router = APIRouter()

class Query(BaseModel):
    text: str

@router.post("/workouts")
def workouts(user: user_dependency, query: Query):
    
    index = pc.Index(os.getenv("PINECONE_INDEX"))
    
    resp = requests.post(
        url=f"{os.getenv("EMBEDDING_API_URL")}/huggingface/embedding",
        json={
            'input': query.text
        }
    )

    embedding = resp.json()['embedding']

    results = index.query(
        vector=embedding,
        top_k=3,
        include_values=False,
        include_metadata=True,
        namespace='workouts'
    )

    final_results = [{'metadata': r['metadata'], 'score': r['score']} for r in results['matches']]

    return { 
        'recommendations': final_results
    }