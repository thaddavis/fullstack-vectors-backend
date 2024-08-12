from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from dotenv import load_dotenv
import os
from db.models import Account
from src.deps import db_dependency, bcrypt_context
from fastapi import Header

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

class AccountCreateRequest(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
def authenticate(email: str, password: str, db):
    account = db.query(Account).filter(Account.email == email).first()
    if not account:
        return False
    if not bcrypt_context.verify(password, account.hashed_password):
        return False
    return account

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_account_request: AccountCreateRequest):
    
    print('...create_user...')
    
    try:
        hashed_password = bcrypt_context.hash(create_account_request.password)
        create_account_model = Account(
            email=create_account_request.email,
            hashed_password=hashed_password
        )
        db.add(create_account_model)
        db.commit()
    except Exception as e:
        print('create_user error', e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    print("login_for_access_token")
    print('form_data.username', form_data.username, 'form_data.password', form_data.password)
    user = authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/validate-token')
async def validate_token(authorization: str = Header(...)):
    try:
        # Extract the token from the 'Bearer' scheme
        token = authorization.split(" ")[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # return {'valid': True, 'user_id': decoded_token['id']}
        return {'access_token': authorization, 'token_type': 'bearer'}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))