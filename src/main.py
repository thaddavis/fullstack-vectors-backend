from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .routers import noRagAgent, ragAgent, reActAgent, healthcheck, auth, workouts, routines

from .db.database import Base, engine

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
app.include_router(workouts.router, prefix="/workouts", tags=['workouts'])
app.include_router(routines.router, prefix="/routines", tags=['routines'])