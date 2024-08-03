from fastapi import APIRouter
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel
from core.schemas.Prompt import Prompt
import os
from langchain.callbacks import LangChainTracer
from langsmith import Client

from dotenv import load_dotenv

load_dotenv()

callbacks = [
  LangChainTracer(
    project_name="completion-agent",
    client=Client(
      api_url=os.getenv("LANGCHAIN_ENDPOINT"),
      api_key=os.getenv("LANGCHAIN_API_KEY")
    )
  )
]

router = APIRouter()

class ResponseBody(BaseModel):
    completion: str

@router.post("/completion")
def prompt(prompt: Prompt) -> ResponseBody:
    model: str = "claude-3-sonnet-20240229"

    llm = ChatAnthropic(
        model_name=model, temperature=0.2, max_tokens=1024
    )

    completion = llm.invoke(prompt.content, config={"callbacks": callbacks}, model=model)

    return {"completion": completion.content}