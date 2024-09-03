from fastapi import APIRouter, Request
# from langchain_anthropic import ChatAnthropic
from langchain_postgres import PostgresChatMessageHistory

from slowapi import Limiter
from slowapi.util import get_remote_address

from core.schemas.SpreadsheetSwarmPrompt import SpreadsheetSwarmPrompt

import json
import os

from fastapi.responses import StreamingResponse

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks import LangChainTracer
import psycopg
from core.swarms.swarms.models.popular_llms import OpenAIChatLLM
from src.deps import jwt_dependency

# vvv SWARM imports vvv
from src.core.swarms.swarms.structs import Agent
from src.core.swarms.swarms.models import Anthropic
from src.core.swarms.swarms.models import OpenAI
from src.core.swarms.swarms.structs.rearrange import AgentRearrange

from src.core.swarms.swarms.utils.loguru_logger import logger

from swarms.models import Anthropic
# ^^^ SWARM imports ^^^

limiter = Limiter(key_func=get_remote_address)

from dotenv import load_dotenv
import uuid

load_dotenv()

callbacks = [
#   LangChainTracer(
#     project_name="streaming-with-memory-agent",
#     client=Client(
#       api_url=os.getenv("LANGCHAIN_ENDPOINT"),
#       api_key=os.getenv("LANGCHAIN_API_KEY")
#     )
#   )
]

router = APIRouter()

async def generator(sessionId: str, prompt: str, agentsConfig: dict):

    print('--- generator ---')

    # llm = Anthropic(anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"), streaming=True)
    llm = OpenAIChatLLM(model='gpt-4o-mini', api_key=os.getenv("OPENAI_API_KEY"))

    # model: str = "claude-3-5-sonnet-20240620"
    # llm = ChatAnthropic(model_name=model, temperature=0.1, max_tokens=1024)
    # conn_info = os.getenv("POSTGRES_URL")
    # sync_connection = psycopg.connect(conn_info)
    # history = PostgresChatMessageHistory(
    #     'chat_history', # table name
    #     sessionId,
    #     sync_connection=sync_connection
    # )
    # promptTemplate = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", "You're an assistant. Bold key terms in your responses."),
    #         MessagesPlaceholder(variable_name="history"),
    #         ("human", "{input}"),
    #     ]
    # )
    # messages = promptTemplate.format_messages(input=prompt, history=history.messages)

    # vvv SEQUENTIAL SWARM vvv

    agents = []
    
    agentsConfigKeys = agentsConfig.keys()

    for agentConfigKey in agentsConfigKeys:
        agents.append(Agent(
            agent_name=agentsConfig[agentConfigKey]['name'],
            system_prompt=agentsConfig[agentConfigKey]['system_prompt'],
            llm=llm,
        ))

    # agents = {agent.name: agent for agent in agents}
    # current_task = prompt

    print(prompt)
    loop_count = 0

    while loop_count < 1:
        results = []
        for agent in agents:

            print('agent', agent.name)

            result = None
            # As the current `swarms` package is using LangChain v0.1 we need to use the v0.1 version of the `astream_events` API
            # Below is the link to the `astream_events` spec as outlined in the LangChain v0.1 docs
            # https://python.langchain.com/v0.1/docs/expression_language/streaming/#event-reference
            # Below is the link to the `astream_events` spec as outlined in the LangChain v0.2 docs
            # https://python.langchain.com/v0.2/docs/versions/v0_2/migrating_astream_events/
            async for evt in agent.astream_events(
                f"SYSTEM: {agent.system_prompt}\nINPUT: {prompt}\nAI: ", version="v1"
            ):
                # print(evt) # <- useful when building/debugging
                
                # if evt["event"] == "on_llm_end":
                #     result = evt["data"]["output"]
                #     print(agent.name, result)

                if evt["event"] == "on_chat_model_start":
                    yield json.dumps({
                        "event": "on_chat_model_start",
                        "run_id": evt['run_id'],
                        "agent_name": agent.name
                    }, separators=(',', ':'))

                elif evt["event"] == "on_chat_model_stream":
                    yield json.dumps({
                        "event": "on_chat_model_stream",
                        "run_id": evt['run_id'],
                        "agent_name": agent.name,
                        "data": evt["data"]['chunk'].content
                    }, separators=(',', ':'))

                elif evt["event"] == "on_chat_model_end":
                    result = evt["data"]["output"].content
                    # print(agent.name, "result", result)
                    yield json.dumps({
                        "event": "on_chat_model_end",
                        "run_id": evt['run_id']
                    }, separators=(',', ':'))
            results.append(result)

            # current_task = ""
            # for index, res in enumerate(results):
            #     print("enumerating...")
                
            #     print('index', index)
            #     print('res', res)

            #     print()
            #     print('--- *** ---')
            #     print()

            #     current_task += (
            #         "# OUTPUT of "
            #         + agents[index].name
            #         + ""
            #         + res
            #         + "\n\n"
            #     )
        loop_count += 1

@router.post("/completion")
@limiter.limit("10/minute")
def prompt(prompt: SpreadsheetSwarmPrompt, jwt: jwt_dependency, request: Request):
    print('/spreadsheet-swarm/completion')
    print(prompt.sessionId, prompt.content, prompt.agentsConfig)
    return StreamingResponse(generator(prompt.sessionId, prompt.content, prompt.agentsConfig), media_type='text/event-stream')