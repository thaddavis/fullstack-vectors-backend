from fastapi import APIRouter
from langchain_anthropic import ChatAnthropic
from core.schemas.ChatSessionPrompt import ChatSessionPrompt

import json
import os
import psycopg

from fastapi.responses import StreamingResponse

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_postgres import PostgresChatMessageHistory
from langchain.callbacks import LangChainTracer
from langsmith import Client

from dotenv import load_dotenv
from pinecone import Pinecone
# from sentence_transformers import SentenceTransformer

load_dotenv()

callbacks = [
  LangChainTracer(
    project_name="rag-agent",
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

    conn_info = os.getenv("POSTGRES_URL")
    sync_connection = psycopg.connect(conn_info)

    history = PostgresChatMessageHistory(
        'chat_history', # table name
        sessionId,
        sync_connection=sync_connection
    )

    # vvv FOR GENERATING EMBEDDINGS WITH HUGGING FACE vvv
    # embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # embeddings = embedding_model.encode([prompt])
    # embeddings_list = embeddings.tolist()
    # ^^^ FOR GENERATING EMBEDDINGS WITH HUGGING FACE ^^^

    # vvv FOR GENERATING EMBEDDINGS WITH OPENAI vvv

    # ^^^ FOR GENERATING EMBEDDINGS WITH OPENAI ^^^

    # pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    # index = pc.Index(os.getenv("PINECONE_INDEX"))

    # results = index.query(
    #     vector=embeddings_list[0],
    #     top_k=3,
    #     include_values=True,
    #     include_metadata=True
    # )

    results = {
        "matches": []
    }

    promptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", "You're an assistant."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )


    prompt_with_relevant_knowledge = "# RELEVANT KNOWLEDGE\n\n" + "\n".join([f"Q: {r['metadata']['q']}\nA: {r['metadata']['a']}" for r in results['matches']]) + "\n\n" + "# PROMPT\n\n" + prompt

    messages = promptTemplate.format_messages(input=prompt_with_relevant_knowledge, history=history.messages)

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