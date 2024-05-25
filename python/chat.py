import os
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.agents import tool

@tool
def calc(expression: str) -> str:
    """Calculate math expression."""
    return eval(expression)


tools = [calc]

from langchain_core.messages import HumanMessage

from langgraph.prebuilt import chat_agent_executor

# response = agent_executor.invoke(
#    {"messages": [HumanMessage(content="1+1は？")]}
# )
# print(response["messages"])

async def initialize_llm(model, temperature):
    return ChatGoogleGenerativeAI(model=model, temperature=temperature)

import asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
llm = loop.run_until_complete(initialize_llm('gemini-1.5-flash', 0.0))

from langgraph.checkpoint import MemorySaver

memory = MemorySaver()
agent_executor = chat_agent_executor.create_tool_calling_executor(
	model = llm, 
	tools = tools,
	checkpointer=memory		
)

config = {"configurable": {"thread_id": "abc123"}}

async def stream_tokens(agent_executor, input, config):
    async for event in agent_executor.astream_events(
        {"messages": [HumanMessage(content=input)]}, version="v1",config=config,
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "LangGraph"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input').get('messages')[0].content}"
                )
        elif kind == "on_chain_end":
            if (
                event["name"] == "LangGraph"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output').get('agent').get('messages')[-1].content}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="", flush=True)
        elif kind == "on_tool_start":
            print("--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")

input = "6400*3200は？"

# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content=input)]}
# ):
#     print(chunk)
#     print("----")

import asyncio
loop.run_until_complete(stream_tokens(agent_executor=agent_executor, input=input, config=config))
loop.close()
