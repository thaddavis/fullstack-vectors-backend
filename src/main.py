from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from . import noRagAgent
from . import ragAgent
from . import reActAgent
from . import healthcheck
from . import auth

from .database import Base, engine

import debugpy

load_dotenv()

debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()

app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "http://agents.com:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(noRagAgent.router, prefix="/no-rag-agent")
app.include_router(ragAgent.router, prefix="/rag-agent")
app.include_router(reActAgent.router, prefix="/react-agent")
app.include_router(healthcheck.router, prefix="")
app.include_router(auth.router, prefix="")