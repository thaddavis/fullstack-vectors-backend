from fastapi import APIRouter, Request
# from langchain_anthropic import ChatAnthropic
from langchain_postgres import PostgresChatMessageHistory

from slowapi import Limiter
from slowapi.util import get_remote_address

from core.schemas.ChatSessionPrompt import ChatSessionPrompt

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

async def generator(sessionId: str, prompt: str, agentsConfig: dict, flowConfig: str):

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

    flow = flowConfig

    # ^^^ SEQUENTIAL SWARM ^^^

    # vvv PARALLEL SWARM vvv

    # writer1 = Agent(
    #   agent_name="J.K. Rowling",
    #   system_prompt="Write in the style of J.K. Rowling",
    #   llm=llm,
    #   dashboard=False,
    # )

    # writer2 = Agent(
    #     agent_name="Stephen King",
    #     system_prompt="Write in the style of Stephen King",
    #     llm=llm,
    #     dashboard=False
    # )

    # writer3 = Agent(
    #     agent_name="Salman Rushdie",
    #     system_prompt="Write in the style of Salman Rushdie",
    #     llm=llm,
    #     dashboard=False
    # )

    # reviewer = Agent(
    #     agent_name="Reviewer",
    #     system_prompt="Select the writer that wrote the best. There can only be one best.",
    #     llm=llm,
    #     dashboard=False
    # )

    # agents = [writer1, writer2, writer3, reviewer]
    # flow = f"{writer1.name}, {writer2.name}, {writer3.name} -> {reviewer.name}"

    # ^^^ PARALLEL SWARM ^^^

    agents = {agent.name: agent for agent in agents}
    tasks = flow.split("->")
    current_task = prompt
    loop_count = 0

    print('tasks', tasks)

    while loop_count < 1:
        for task in tasks:

            print('task', task)

            agent_names = [
                name.strip() for name in task.split(",")
            ]
            if len(agent_names) > 1:
                # Parallel processing
                print(
                    f"Running agents in parallel: {agent_names}"
                )

                parallel_group_id = str(uuid.uuid4())

                results = []
                for agent_name in agent_names:
                    agent = agents[agent_name]
                    result = None
                    # As the current `swarms` package is using LangChain v0.1 we need to use the v0.1 version of the `astream_events` API
                    # Below is the link to the `astream_events` spec as outlined in the LangChain v0.1 docs
                    # https://python.langchain.com/v0.1/docs/expression_language/streaming/#event-reference
                    # Below is the link to the `astream_events` spec as outlined in the LangChain v0.2 docs
                    # https://python.langchain.com/v0.2/docs/versions/v0_2/migrating_astream_events/
                    async for evt in agent.astream_events(
                        current_task, version="v1"
                    ):
                        # print(evt) # <- useful when building/debugging
                        
                        # if evt["event"] == "on_llm_end":
                        #     result = evt["data"]["output"]
                        #     print(agent.name, result)

                        if evt["event"] == "on_chat_model_start":
                            yield json.dumps({
                                "parallel_group_id": parallel_group_id,
                                "event": "on_chat_model_start",
                                "run_id": evt['run_id'],
                                "agent_name": agent.name
                            }, separators=(',', ':'))

                        elif evt["event"] == "on_chat_model_stream":
                            yield json.dumps({
                                "parallel_group_id": parallel_group_id,
                                "event": "on_chat_model_stream",
                                "run_id": evt['run_id'],
                                "agent_name": agent.name,
                                "data": evt["data"]['chunk'].content
                            }, separators=(',', ':'))

                        elif evt["event"] == "on_chat_model_end":
                            result = evt["data"]["output"].content
                            print(agent.name, "result", result)
                            yield json.dumps({
                                "event": "on_chat_model_end",
                                "run_id": evt['run_id']
                            }, separators=(',', ':'))
                    results.append(result)

                current_task = ""
                for index, res in enumerate(results):
                    print("enumerating...")
                    
                    print('index', index)
                    
                    print('agent_names', agent_names),
                    print('res', res)

                    print()
                    print('--- *** ---')
                    print()

                    current_task += (
                        "# OUTPUT of "
                        + agent_names[index]
                        + ""
                        + res
                        + "\n\n"
                    )
            else:
                # Sequential processing
                print(
                    f"Running agents sequentially: {agent_names}"
                )
                agent_name = agent_names[0]
                agent = agents[agent_name]
                result = None

                # As the current `swarms` package is using LangChain v0.1 we need to use the v0.1 version of the `astream_events` API
                # Below is the link to the `astream_events` spec as outlined in the LangChain v0.1 docs
                # https://python.langchain.com/v0.1/docs/expression_language/streaming/#event-reference
                # Below is the link to the `astream_events` spec as outlined in the LangChain v0.2 docs
                # https://python.langchain.com/v0.2/docs/versions/v0_2/migrating_astream_events/
                async for evt in agent.astream_events(
                    f"SYSTEM: {agent.system_prompt}\nINPUT: {current_task}\nAI: ",
                    version="v1",
                ):
                    # print(evt) # <- useful when building/debugging

                    if evt["event"] == "on_chat_model_start":
                        yield json.dumps({
                            "event": "on_chat_model_start",
                            "run_id": evt['run_id'],
                            "agent_name": agent.name
                        }, separators=(',', ':'))

                    elif evt["event"] == "on_chat_model_stream":
                        yield json.dumps({
                            "event": "on_chat_model_stream",
                            "data": evt["data"]['chunk'].content,
                            "run_id": evt['run_id']
                        }, separators=(',', ':'))

                    elif evt["event"] == "on_chat_model_end":
                        result = evt["data"]["output"].content
                        print(agent.name, "result", result)
                        yield json.dumps({
                            "event": "on_chat_model_end",
                            "run_id": evt['run_id']
                        }, separators=(',', ':'))

                        # raise StopAsyncIteration
                    
                current_task = result
        loop_count += 1

@router.post("/completion")
@limiter.limit("10/minute")
def prompt(prompt: ChatSessionPrompt, jwt: jwt_dependency, request: Request):
    print('/sequential-swarm/completion')
    print(prompt.sessionId, prompt.content, prompt.agentsConfig, prompt.flow)
    return StreamingResponse(generator(prompt.sessionId, prompt.content, prompt.agentsConfig, prompt.flow), media_type='text/event-stream')