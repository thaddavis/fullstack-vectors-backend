from fastapi import APIRouter
from langchain_anthropic import ChatAnthropic
from core.schemas.Prompt import Prompt
import json
import os

from fastapi.responses import StreamingResponse

from langchain.callbacks import LangChainTracer
from langsmith import Client

from dotenv import load_dotenv

load_dotenv()

callbacks = [
  LangChainTracer(
    project_name="streaming-agent",
    client=Client(
      api_url=os.getenv("LANGCHAIN_ENDPOINT"),
      api_key=os.getenv("LANGCHAIN_API_KEY")
    )
  )
]

router = APIRouter()

async def generator(prompt: str):
    model: str = "claude-3-sonnet-20240229"
    llm = ChatAnthropic(model_name=model, temperature=0.2, max_tokens=1024)
    
    # EVENTS <!-- https://python.langchain.com/docs/expression_language/streaming/#event-reference -->
    # on_chat_model_start, on_chat_model_stream, on_chat_model_end, on_llm_start, on_llm_stream, on_llm_end, on_chain_start, on_chain_stream, on_chain_end
    # on_tool_start, on_tool_stream, on_tool_end, on_retriever_start, on_retriever_chunk, on_retriever_end, on_prompt_start, on_prompt_end

    async for evt in llm.astream_events(prompt, version="v1", config={"callbacks": callbacks}, model=model):
        if evt["event"] == "on_chat_model_start":
            yield json.dumps({
                "event": "on_chat_model_start"
            }, separators=(',', ':'))

        elif evt["event"] == "on_chat_model_stream":
            yield json.dumps({
                "event": "on_chat_model_stream",
                "data": evt["data"]['chunk'].content
            }, separators=(',', ':'))

        elif evt["event"] == "on_chat_model_end":
            yield json.dumps({
                "event": "on_chat_model_end"
            }, separators=(',', ':'))

@router.post("/completion")
def prompt(prompt: Prompt):
    return StreamingResponse(generator(prompt.content), media_type='text/event-stream')