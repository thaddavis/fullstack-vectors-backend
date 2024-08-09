from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/")
def health_check(response: Response):
    response.status_code = 200
    return {"status": "OK!"}