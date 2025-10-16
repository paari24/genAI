from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image as AGImage

from PIL import Image
from io import BytesIO
import requests
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o-mini")

assistant = AssistantAgent(name="my_Assistant", model_client=model_client,
                               description="Image Analyst",
                               system_message="You are a helpful assistant" \
                               "Analyse the image and answer the questions about it."
                               )

async def multi_model_task():
    response = requests.get("https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d")
    image = Image.open(BytesIO(response.content))
    ag_image = AGImage(image)
    multimodel_message = MultiModalMessage(content=["what is the image about", ag_image], source="user")
    response = await assistant.run(task=multimodel_message)
    print(response.messages[-1].content)

asyncio.run(multi_model_task())