from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken

from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o-mini")

def get_weather (city:str) -> str:#-> str it is return type hint
    # Dummy implementation for example purposes
    return f"The current weather in {city} is sunny with a temperature of 25°C."

assistant = AssistantAgent(name="my_Assistant", model_client=model_client,
                               description="Weather Assistant",
                               system_message="You are a weather assistant use " \
                               "the get_weather tool to find the weather of a city.",
                               tools={get_weather})

async def assistat_task():
    await Console(assistant.on_messages_stream(
        messages=[TextMessage(role="user", content="Get weather for chennai", source="user")],
        cancellation_token=CancellationToken()
    ),
    output_stats=True)
     
asyncio.run(assistat_task())