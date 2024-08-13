from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, BackgroundTasks, Request
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from dotenv import load_dotenv
import os
import hashlib
from db.models import Account, Logins
from services import fetch_embedding
from src.deps import db_dependency, bcrypt_context
from pinecone import Pinecone

load_dotenv()

router = APIRouter()

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

# BACKGROUND JOB FOR RECORDING LOGIN
async def record_login(account_id: int, account_email: str, ip_address: str, db):
    print(f"Recording login for account... ")

    created_at = datetime.now()
    log = f"{ip_address} {created_at}"
    
    embedding = await fetch_embedding(log) # fetch embedding from EMBEDDING_API_URL

    print('embedding', len(embedding))

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX"))

    # Compare the log with the existing logs

    results = index.query(
        vector=embedding,
        top_k=1,
        include_values=False,
        include_metadata=True,
        namespace='logins',
        filter={
          "email": {"$eq": account_email}
        },
    )

    similarity_threshold = 0.6
    is_suspicous = False

    if len(results['matches']) > 0:
        print("login similarity score", results['matches'][0]['score'])
        print("is_suspicious", results['matches'][0]['score'] < similarity_threshold)
        print("log", log)

        is_suspicous = True if results['matches'][0]['score'] < similarity_threshold else False

    db.add(Logins(account_id=account_id, ip_address=ip_address,is_suspicious=is_suspicous))
    db.commit()

    # Insert the log into the Pinecone index
    
    index.upsert(
        vectors=[
            {
                "id": hashlib.sha1(log.encode('utf-8')).hexdigest(),
                "values": embedding,
                "metadata": {"email": account_email, "ip_address": ip_address, "created_at": created_at}
            },
        ],
        namespace='logins'
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_account_request: AccountCreateRequest):
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
    

@router.post('/login')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency,
                                 request: Request,
                                 background_tasks: BackgroundTasks):
    account = authenticate(form_data.username, form_data.password, db)
    if not account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    # Record the login in the background
    ip_address = request.client.host
    background_tasks.add_task(record_login, account.id, account.email, ip_address, db)

    token = create_access_token(account.email, account.id, timedelta(minutes=20))
    response = Response()    
    response.set_cookie(key="jwt", value=token, httponly=True, expires=60*20, secure=True, samesite="none", path="/") 
    return response


@router.get('/validate-token')
async def validate_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1] # Extract the token from the 'Bearer' scheme
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {'access_token': authorization, 'token_type': 'bearer'}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
@router.post("/logout")
def logout(response: Response):
    response.set_cookie(
        key="jwt",
        value="",
        httponly=True,
        secure=True,
        samesite="None",
        path="/",
        max_age=0  # Setting max_age to 0 effectively deletes the cookie
    )
    return {"message": "Logged out successfully"}