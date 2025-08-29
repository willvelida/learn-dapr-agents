# Stateful LLM Pattern Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd patterns\stateful-llm
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

**Prerequisites:**
```powershell
# Start Redis for state storage
docker run -d --name redis-stateful -p 6379:6379 redis

# Initialize Dapr
dapr init
```

---

## Demo: Stateful LLM Pattern
**File:** `app.py`

This demonstrates the Stateful LLM pattern - persistent memory with durable agent services.

```powershell
dapr run --app-id book-buddy --app-port 8002 --dapr-http-port 3500 --resources-path .\components\ -- python app.py
```

**Test the agent (in another terminal):**
```powershell
# First interaction - establish preferences
curl -X POST http://localhost:8002/start-workflow -H "Content-Type: application/json" -d "{\"task\": \"I love fantasy novels\"}"

# Second interaction - use memory and tools
curl -X POST http://localhost:8002/start-workflow -H "Content-Type: application/json" -d "{\"task\": \"Can you recommend something to read?\"}"
```

**Key Features:**
- **Persistent Memory** - `ConversationDaprStateMemory` remembers user preferences
- **Tool Integration** - Book recommendation tool with structured data
- **Durable Agent** - Full workflow capabilities with state persistence
- **REST API** - Service endpoints for external integration

**Pattern Benefits:**
- **Context Preservation** - Memory survives agent restarts and sessions
- **Personalization** - Tailored responses based on user history
- **Service Architecture** - RESTful endpoints for integration
- **Durability** - State persisted across failures and deployments

**Use Cases:**
- Personal assistants with long-term memory
- Customer service chatbots
- Recommendation systems
- Educational tutoring agents
- Healthcare monitoring assistants

This pattern shows how to build production-ready agents with persistent memory and service capabilities for real-world applications.
