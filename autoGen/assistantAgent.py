from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

async def main():
    model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4")
    assistant = AssistantAgent(name="my_Assistant", model_client=model_client)
    response = await assistant.run(task="Tell a joke")
    print(response.messages[-1].content)

asyncio.run(main())