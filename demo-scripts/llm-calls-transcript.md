# Dapr Agents LLM Calls Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd lessons\llm-calls
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

---

## Demo 1: Basic LLM Chat
**File:** `basic_llm_chat.py`

This demonstrates the simplest way to interact with LLMs using Dapr Agents.

```powershell
python basic_llm_chat.py
```

**Key Points:**
- Uses `DaprChatClient` for basic LLM interactions
- Two patterns: simple string input and structured `UserMessage`
- Foundation for all LLM-based applications
- Shows basic response handling and validation

---

## Demo 2: Streaming Responses
**File:** `streaming_responses.py`

This shows how to handle streaming responses for real-time user feedback.

```powershell
python streaming_responses.py
```

**Key Points:**
- Uses `OpenAIChatClient` with `stream=True` parameter
- Returns `Iterator[LLMChatResponseChunk]` for real-time processing
- Perfect for chat applications with typing indicators
- Demonstrates chunk-by-chunk content processing

---

## Demo 3: Streaming with Tools
**File:** `streaming_with_tools.py`

This demonstrates advanced streaming with function calling capabilities.

```powershell
python streaming_with_tools.py
```

**Key Points:**
- Combines streaming responses with tool execution
- Shows weather lookup tool integration
- Handles tool call accumulation across chunks
- Demonstrates conversation flow with tool results
- Real-world pattern for interactive AI applications

---

## Demo 4: Structured Completion
**File:** `structured_completion_to_pydantic.py`

This shows how to get structured responses using Pydantic models.

```powershell
python structured_completion_to_pydantic.py
```

**Key Points:**
- Uses `response_format` parameter with Pydantic models
- Ensures type-safe, structured responses
- Perfect for data extraction and API responses
- No manual JSON parsing required

---

## Component Configuration
The examples use Dapr components for LLM configuration:

**OpenAI Component (`components/openai.yaml`):**
- Configures OpenAI connection with API key
- Sets model and caching parameters
- Production-ready configuration

**Echo Component (`components/echo.yaml`):**
- Simple test component for development
- Useful for testing without API costs

---

## Summary
These examples demonstrate the core LLM interaction patterns with Dapr Agents:

1. **Basic Chat** - Simple request-response pattern
2. **Streaming** - Real-time response processing
3. **Tools Integration** - Function calling with streaming
4. **Structured Output** - Type-safe responses with Pydantic

Each pattern builds foundational skills for building production AI applications with Dapr Agents.
