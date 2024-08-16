from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
import replicate
from src.deps import jwt_dependency
import os
from core.clients import pc

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

class Query(BaseModel):
    text: str

@router.post("/media-assets/query")
@limiter.limit("10/minute")
def media_library(request: Request, response: Response, jwt: jwt_dependency, query: Query):
    
    output = replicate.run(
        "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
        input={
            # vvv vvv vvv
            "modality": "text",
            "text_input": query.text,
            # ^^^ ^^^ ^^^
        }
    )

    index = pc.Index(os.getenv("PINECONE_IMAGEBIND_1024_DIMS_INDEX"))

    results = index.query(
        vector=output,
        top_k=3,
        include_values=False,
        include_metadata=True,
        namespace='media_assets'
    )

    final_results = []
    for r in results['matches']:
        final_results.append({'metadata': r['metadata'], 'score': r['score']})

    response.status_code = 200
    return {"results": final_results}

