from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4")

def get_weather (city:str) -> str:#-> str it is return type hint
    # Dummy implementation for example purposes
    return f"The current weather in {city} is sunny with a temperature of 25°C."

assistant = AssistantAgent(name="my_Assistant", model_client=model_client,
                               description="Weather Assistant",
                               system_message="You are a weather assistant use the get_weather tool to find the weather of a city.",
                               tools={get_weather})

async def get_weather():
    response = await assistant.run(task="Get weather for chennai")
    print(response.messages[-1].content)

asyncio.run(get_weather())