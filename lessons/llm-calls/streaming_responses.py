from dotenv import load_dotenv
from dapr_agents import OpenAIChatClient
from dapr_agents.types.message import LLMChatResponseChunk
from typing import Iterator
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

llm = OpenAIChatClient()

response: Iterator[LLMChatResponseChunk] = llm.generate("Give me a New York Times bestselling book", stream=True)

for chunk in response:
    if chunk.result.content:
        print(chunk.result.content, end="", flush=True)