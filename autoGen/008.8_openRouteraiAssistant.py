from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

openRouter_api_key = os.getenv("OPENROUTER_API_KEY")

open_router_client = OpenAIChatCompletionClient(
    api_key=openRouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-oss-20b:free",
        model_info={
            "family": "openai",
            "version": "20b",
            "vision": False,
            "function_calling": False,
            "json_output": True,
            "structured_output": False  # Added to resolve warning
        }
    )

assistant = AssistantAgent(
    name="my_Assistant", model_client=open_router_client,
    system_message="You are a helpful assistant."
    )

async def chat(question):
    response = await assistant.run(task=question)
    print(response.messages[-1].content)

asyncio.run(chat("How areyou?"))