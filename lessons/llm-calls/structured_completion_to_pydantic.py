import json
from dotenv import load_dotenv
from pydantic import BaseModel
from dapr_agents import OpenAIChatClient
from dapr_agents.types import UserMessage

load_dotenv()

class Book(BaseModel):
    title: str
    author: str
    genre: str

llm = OpenAIChatClient()

response: Book = llm.generate(
    messages=[UserMessage("Give me a New York Times bestselling book")], response_format=Book
)

print(json.dumps(response.model_dump(), indent=2))