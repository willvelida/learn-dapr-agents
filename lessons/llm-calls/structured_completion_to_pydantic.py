import json
from dotenv import load_dotenv
from pydantic import BaseModel
from dapr_agents import OpenAIChatClient
from dapr_agents.types import UserMessage

# Load environment variables
load_dotenv()

# Define our data set
class Book(BaseModel):
    title: str
    author: str
    genre: str

# Initialize the chat client
llm = OpenAIChatClient()

# Get our structured response
response: Book = llm.generate(
    messages=[UserMessage("Give me a New York Times bestselling book")], response_format=Book
)

print(json.dumps(response.model_dump(), indent=2))