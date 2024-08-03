from fastapi import APIRouter
from langchain_anthropic import ChatAnthropic
from core.schemas.ChatSessionPrompt import ChatSessionPrompt

import json
import os

from fastapi.responses import StreamingResponse

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.callbacks import LangChainTracer
from langsmith import Client

from dotenv import load_dotenv

load_dotenv()

callbacks = [
  LangChainTracer(
    project_name="streaming-with-memory-agent",
    client=Client(
      api_url=os.getenv("LANGCHAIN_ENDPOINT"),
      api_key=os.getenv("LANGCHAIN_API_KEY")
    )
  )
]

router = APIRouter()

async def generator(sessionId: str, prompt: str):
    model: str = "claude-3-sonnet-20240229"
    llm = ChatAnthropic(model_name=model, temperature=0.2, max_tokens=1024)

    history = RedisChatMessageHistory(sessionId, url=os.getenv("REDIS_URL"))
    
    print('history.message', history.messages)

    promptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", "You're an assistant."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )

    messages = promptTemplate.format_messages(input=prompt, history=history.messages)

    async for evt in llm.astream_events(messages, version="v1", config={"callbacks": callbacks}, model=model):
        if evt["event"] == "on_chat_model_start":
            history.add_user_message(prompt)

            yield json.dumps({
                "event": "on_chat_model_start"
            }, separators=(',', ':'))

        elif evt["event"] == "on_chat_model_stream":
            yield json.dumps({
                "event": "on_chat_model_stream",
                "data": evt["data"]['chunk'].content
            }, separators=(',', ':'))

        elif evt["event"] == "on_chat_model_end":
            history.add_ai_message(evt['data']['output'].content)

            yield json.dumps({
                "event": "on_chat_model_end"
            }, separators=(',', ':'))

@router.post("/completion")
def prompt(prompt: ChatSessionPrompt):
    
    return StreamingResponse(generator(prompt.sessionId, prompt.content), media_type='text/event-stream')