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
from src.deps import jwt_dependency

# vvv SWARM imports vvv
from src.core.swarms.swarms.structs import Agent
from src.core.swarms.swarms.models import Anthropic
from src.core.swarms.swarms.structs.rearrange import AgentRearrange

from src.core.swarms.swarms.utils.loguru_logger import logger

from swarms.models import Anthropic
# ^^^ SWARM imports ^^^

limiter = Limiter(key_func=get_remote_address)

from dotenv import load_dotenv

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

async def generator(sessionId: str, prompt: str):

    print("--- generator ---")

    llm = Anthropic(anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"), streaming=True)

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

    print("--- 222 ---")

    agent1 = Agent(
        agent_name="Blog generator",
        system_prompt="Generate a blog post like stephen king",
        llm=llm,
        dashboard=False,
        streaming_on=True
    )

    agent2 = Agent(
        agent_name="Summarizer",
        system_prompt="Summarize the blog post",
        llm=llm,
        dashboard=False,
        streaming_on=True
    )

    agents = [agent1, agent2]

    flow = f"{agent1.name} -> {agent2.name}"

    # --- --- --- --- --- --- --- --- --- --- ---

    agents = {agent.name: agent for agent in agents}

    # --- --- --- --- --- --- --- --- --- --- ---

    print("--- 333 ---")

    tasks = flow.split("->")
    current_task = prompt
    loop_count = 0

    print("--- 444 ---")

    while loop_count < 1:
        for task in tasks:
            agent_names = [
                name.strip() for name in task.split(",")
            ]
            if len(agent_names) > 1:
                # Parallel processing
                print(
                    f"Running agents in parallel: {agent_names}"
                )
                results = []
                for agent_name in agent_names:
                    # if agent_name == "H":
                    #     # Human in the loop intervention
                    #     if (
                    #         self.human_in_the_loop
                    #         and self.custom_human_in_the_loop
                    #     ):
                    #         current_task = (
                    #             self.custom_human_in_the_loop(
                    #                 current_task
                    #             )
                    #         )
                    #     else:
                    #         current_task = input(
                    #             "Enter your response:"
                    #         )
                    # else:
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
                        if evt["event"] == "on_llm_end":
                            result = evt["data"]["output"]
                            print(agent.name, result)
                    results.append(result)

                current_task = ""
                for index, res in enumerate(results):
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

                print('1')
                
                print('agent_name', agent_name)
                print('agents', agents)


                agent = agents[agent_name]

                print('2')

                result = None

                print('3')
                # As the current `swarms` package is using LangChain v0.1 we need to use the v0.1 version of the `astream_events` API
                # Below is the link to the `astream_events` spec as outlined in the LangChain v0.1 docs
                # https://python.langchain.com/v0.1/docs/expression_language/streaming/#event-reference
                # Below is the link to the `astream_events` spec as outlined in the LangChain v0.2 docs
                # https://python.langchain.com/v0.2/docs/versions/v0_2/migrating_astream_events/

                print("--- 555 ---")

                async for evt in agent.astream_events(
                    f"SYSTEM: {agent.system_prompt}\nINPUT:{current_task}",
                    version="v1",
                ):
                    print(evt) # <- useful when building/debugging

                    if evt["event"] == "on_llm_start":
                        yield json.dumps({
                            "event": "on_llm_start",
                            "run_id": evt['run_id']
                        }, separators=(',', ':'))

                    elif evt["event"] == "on_llm_stream":
                        yield json.dumps({
                            "event": "on_llm_stream",
                            "data": evt["data"]['chunk'],
                            "run_id": evt['run_id']
                        }, separators=(',', ':'))

                    elif evt["event"] == "on_llm_end":
                        result = evt["data"]["output"]
                        print(agent.name, "result", result)
                        yield json.dumps({
                            "event": "on_llm_end",
                            "run_id": evt['run_id']
                        }, separators=(',', ':'))
                    
                current_task = result

        loop_count += 1

    # return current_task

    # --- --- --- --- --- --- --- --- --- --- ---

    # yield await agent_rearrange.astream(
    #     "Generate a short blog post about Muhammad Ali."
    # )

    # LEAVING THIS CALL BELOW FOR COMPARISON with "completion-style" .run() approach ;)
    # await agent_rearrange.run(
    #   "Generate a short blog post about Muhammad Ali."
    # )

    # async for evt in llm.astream_events('Hey Buddy!', version="v1", config={"callbacks": callbacks}, model=model):
    #     if evt["event"] == "on_chat_model_start":
    #         # history.add_user_message(prompt)

    #         yield json.dumps({
    #             "event": "on_chat_model_start"
    #         }, separators=(',', ':'))

    #     elif evt["event"] == "on_chat_model_stream":
    #         yield json.dumps({
    #             "event": "on_chat_model_stream",
    #             "data": evt["data"]['chunk'].content
    #         }, separators=(',', ':'))

    #     elif evt["event"] == "on_chat_model_end":
    #         # history.add_ai_message(evt['data']['output'].content)

    #         yield json.dumps({
    #             "event": "on_chat_model_end"
    #         }, separators=(',', ':'))

@router.post("/completion")
@limiter.limit("10/minute")
def prompt(prompt: ChatSessionPrompt, jwt: jwt_dependency, request: Request):
    print('/sequential-swarm/completion')
    print(prompt.sessionId, prompt.content)
    return StreamingResponse(generator(prompt.sessionId, prompt.content), media_type='text/event-stream')