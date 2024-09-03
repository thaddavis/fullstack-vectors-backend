from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

# from .routers import noRagAgent, ragAgent, reActAgent, healthcheck, auth, recommendations, logins, multimodal, sequentialSwarm
from .routers import noRagAgent, healthcheck, auth, recommendations, logins, multimodal, rearrangeSwarm, spreadsheetSwarm

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
    "https://wishbliss.link",
    "https://fullstack-rag-nextjs-service-esw7hvt5nq-ue.a.run.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a Limiter instance
limiter = Limiter(key_func=get_remote_address)

# Add SlowAPI middleware to FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(healthcheck.router, prefix="")

app.include_router(
    noRagAgent.router,
    prefix="/no-rag-agent",
)
# app.include_router(
#     ragAgent.router,
#     prefix="/rag-agent",
# )
# app.include_router(
#     reActAgent.router,
#     prefix="/react-agent",
# )

# app.include_router(
#     auth.router,
#     prefix='/auth',
#     tags=['auth'],
# )

app.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=['recommendations'],
)
app.include_router(
    logins.router,
    prefix="/logins",
    tags=['logins'],
)

app.include_router(
    multimodal.router,
    prefix="/multi-modal",
    tags=['multimodal'],
)

app.include_router(
    rearrangeSwarm.router,
    prefix="/rearrange-swarm",
    tags=['Sequential Swarm'],
)

app.include_router(
    spreadsheetSwarm.router,
    prefix="/spreadsheet-swarm",
    tags=['Spreadsheet Swarm'],
)