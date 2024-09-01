from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from .db.database import SessionLocal
from fastapi import Request

load_dotenv()

SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
ALGORITHM = os.getenv('AUTH_ALGORITHM')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=["sha256_crypt"])

async def get_current_user(request: Request):
    try:

        print("get_current_user")

        token = request.cookies.get("jwt")

        print("token", token)

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        print('--- SECRET_KEY ---', SECRET_KEY)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print()
        print('--- payload ---', payload)
        print()

        email: str = payload.get('sub')
        account_id: str = payload.get('id')
        
        print('--- email (sub) ---', email)
        
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'username': email, 'id': account_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
jwt_dependency = Annotated[dict, Depends(get_current_user)]