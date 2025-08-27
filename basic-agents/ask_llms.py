from dotenv import load_dotenv
from dapr_agents import OpenAIChatClient
from dapr_agents.types.message import LLMChatResponse

# Load environment variables (including OPENAI_API_KEY)
load_dotenv()

# Create the OpenAI chat client
llm = OpenAIChatClient()

# Generate a response from the LLM
response: LLMChatResponse = llm.generate("Does Dapr have a Agent framework?")

# Extract and print the response content
if response.get_message() is not None:
    content = response.get_message().content
    print("Response:", content)