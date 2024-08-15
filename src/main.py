from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .routers import noRagAgent, ragAgent, reActAgent, healthcheck, auth, recommendations, logins, multimodal

from .db.database import Base, engine

import debugpy

load_dotenv()

# debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()

app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "https://thealignmentagency.com",
    "https://fullstack-rag-nextjs-service-esw7hvt5nq-ue.a.run.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck.router, prefix="")

app.include_router(noRagAgent.router, prefix="/no-rag-agent")
app.include_router(ragAgent.router, prefix="/rag-agent")
app.include_router(reActAgent.router, prefix="/react-agent")

app.include_router(auth.router, prefix='/auth', tags=['auth'])

app.include_router(recommendations.router, prefix="/recommendations", tags=['recommendations'])
app.include_router(logins.router, prefix="/logins", tags=['logins'])

app.include_router(multimodal.router, prefix="/multi-modal", tags=['multimodal'])