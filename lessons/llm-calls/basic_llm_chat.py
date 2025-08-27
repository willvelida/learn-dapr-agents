from dotenv import load_dotenv

from dapr_agents.llm import DaprChatClient
from dapr_agents.types import LLMChatResponse, UserMessage

load_dotenv()

# Basic chat completion
llm = DaprChatClient()
response: LLMChatResponse = llm.generate("Give me a recipe for cheesecake")

if response.get_message() is not None:
    print("Response: ", response.get_message().content)

# Chat completion with user input
llm = DaprChatClient()
response: LLMChatResponse = llm.generate(messages=[UserMessage("hello there!")])

if (
    response.get_message() is not None and "hello there!" in response.get_message().content.lower()
):
    print("Response with user input: ", response.get_message().content)