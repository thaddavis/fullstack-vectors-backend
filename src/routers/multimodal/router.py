from fastapi import APIRouter, Response
from pydantic import BaseModel
import replicate
from src.deps import jwt_dependency
import os
from core.clients import pc

router = APIRouter()

class Query(BaseModel):
    text: str

@router.post("/media-assets/query")
def media_library(response: Response, jwt: jwt_dependency, query: Query):
    
    print('---> query <---', query.text)

    output = replicate.run(
        "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
        input={
            # vvv TEXT EXAMPLE vvv
            "modality": "text",
            "text_input": query.text,
            # ^^^ ^^^ ^^^
            # vvv IMAGE EXAMPLE vvv
            # "modality": "vision",
            # "input": input
            # ^^^ ^^^ ^^^
        }
    )

    index = pc.Index(os.getenv("PINECONE_IMAGEBIND_1024_DIMS_INDEX"))

    # print('output', output)
    print()
    print(len(output))
    print()

    results = index.query(
        vector=output,
        top_k=3,
        include_values=False,
        include_metadata=True,
        namespace='media_assets'
    )

    print()
    print('results', results)
    print()

    final_results = []
    for r in results['matches']:
        final_results.append({'metadata': r['metadata'], 'score': r['score']})

    response.status_code = 200
    return {"results": final_results}

