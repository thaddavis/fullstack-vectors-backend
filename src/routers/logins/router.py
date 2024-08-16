from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Request, status

from src.db.models import Logins
from src.deps import db_dependency, jwt_dependency

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get('/')
@limiter.limit("10/minute")
def get_logins(db: db_dependency, jwt: jwt_dependency, request: Request):
    return db.query(Logins).filter(Logins.account_id == jwt.get('id')).order_by(Logins.created_at.desc()).all()
