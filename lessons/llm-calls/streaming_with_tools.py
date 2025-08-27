from dotenv import load_dotenv
from dapr_agents import OpenAIChatClient
from dapr_agents.types.message import LLMChatResponseChunk
from typing import Iterator
import logging
import json

logging.basicConfig(level=logging.INFO)
load_dotenv()

llm = OpenAIChatClient()

# Simulated weather lookup tool
def get_weather(city: str) -> str:
    # In a real app, you'd call an API here
    return f"The weather in {city} is sunny with a high of 25°C."

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Name of the city"}
            },
            "required": ["city"]
        }
    }
}

messages = [
    {"role": "system", "content": "You are a weather-savvy assistant."},
    {"role": "user", "content": "What's the weather like in Melbourne today?"}
]

print("Getting weather information...\n")

response: Iterator[LLMChatResponseChunk] = llm.generate(messages=messages, tools=[weather_tool], stream=True)

# Collect tool calls and content
tool_calls = {}
content_parts = []

for chunk in response:
    chunk_data = chunk.result
    
    # Handle tool calls
    if hasattr(chunk_data, 'tool_calls') and chunk_data.tool_calls:
        for tool_call in chunk_data.tool_calls:
            if tool_call.index not in tool_calls:
                tool_calls[tool_call.index] = {
                    'id': tool_call.id,
                    'type': tool_call.type,
                    'function': {
                        'name': tool_call.function.name if tool_call.function.name else '',
                        'arguments': ''
                    }
                }
            
            # Accumulate function arguments
            if tool_call.function.arguments:
                tool_calls[tool_call.index]['function']['arguments'] += tool_call.function.arguments
    
    # Handle regular content
    if hasattr(chunk_data, 'content') and chunk_data.content:
        content_parts.append(chunk_data.content)
        print(chunk_data.content, end='', flush=True)

print()  # New line after streaming content

# Process tool calls if any were made
if tool_calls:
    print("\nProcessing tool calls...")
    
    # Add the assistant's message with tool calls to conversation
    messages.append({
        "role": "assistant",
        "tool_calls": [
            {
                "id": call_data['id'],
                "type": call_data['type'],
                "function": {
                    "name": call_data['function']['name'],
                    "arguments": call_data['function']['arguments']
                }
            }
            for call_data in tool_calls.values()
        ]
    })
    
    # Execute each tool call
    for call_data in tool_calls.values():
        function_name = call_data['function']['name']
        function_args = json.loads(call_data['function']['arguments'])
        
        print(f"Calling {function_name} with arguments: {function_args}")
        
        # Execute the function (in a real app, you'd have a dispatch mechanism)
        if function_name == "get_weather":
            result = get_weather(**function_args)
        else:
            result = f"Unknown function: {function_name}"
        
        print(f"Function result: {result}")
        
        # Add tool result to conversation
        messages.append({
            "role": "tool",
            "tool_call_id": call_data['id'],
            "content": result
        })
    
    # Get final response from LLM
    print("\nGetting final response...\n")
    final_response: Iterator[LLMChatResponseChunk] = llm.generate(messages=messages, tools=[weather_tool], stream=True)
    
    for chunk in final_response:
        if hasattr(chunk.result, 'content') and chunk.result.content:
            print(chunk.result.content, end='', flush=True)
    
    print("\n")
else:
    # If no tool calls, just print the accumulated content
    if content_parts:
        print("".join(content_parts))