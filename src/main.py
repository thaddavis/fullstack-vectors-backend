from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from . import _1_completionAgent
from . import _2_streamingAgent
from . import _3_streamingWithMemoryAgent
from . import _4_ragAgent
from . import _5_reActAgent

import debugpy

load_dotenv()

debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()

app = FastAPI()

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

app.include_router(_1_completionAgent.router, prefix="/completion-agent")
app.include_router(_2_streamingAgent.router, prefix="/streaming-agent")
app.include_router(_3_streamingWithMemoryAgent.router, prefix="/streaming-with-memory-agent")
app.include_router(_4_ragAgent.router, prefix="/rag-agent")
app.include_router(_5_reActAgent.router, prefix="/react-agent")