from fastapi import APIRouter, Response
from pydantic import BaseModel
import replicate
from src.deps import db_dependency, jwt_dependency

router = APIRouter()

class Query(BaseModel):
    text: str

@router.post("/media-assets/query")
def media_library(response: Response, jwt: jwt_dependency, query: Query):
    
    # output = replicate.run(
    #     "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
    #     input={
    #         # vvv TEXT EXAMPLE vvv
    #         "modality": "text",
    #         "text_input": query.text,
    #         # ^^^ ^^^ ^^^
    #         # vvv IMAGE EXAMPLE vvv
    #         # "modality": "vision",
    #         # "input": input
    #         # ^^^ ^^^ ^^^
    #     }
    # )

    # print(len(output))

    response.status_code = 200
    return {"status": "OK!"}

