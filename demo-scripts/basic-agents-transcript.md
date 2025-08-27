# Dapr Agents Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

---

## Demo 1: Basic LLM Usage
**File:** `ask_llms.py`

This shows the simplest way to interact with OpenAI using Dapr Agents.

```powershell
python ask_llms.py
```

**Key Points:**
- Direct LLM interaction with `OpenAIChatClient`
- Simple question-answer pattern
- Foundation for all other examples

---

## Demo 2: Simple Agent with Tools
**File:** `simple_agent_tools.py`

This demonstrates creating an agent with custom tools.

```powershell
python simple_agent_tools.py
```

**Key Points:**
- `@tool` decorator for custom functions
- Agent combines LLM with tools and instructions
- Tool returns mock stock price data

---

## Demo 3: Durable Agent
**File:** `durable_agents.py`

This shows a stateful agent with persistent memory using Dapr components.

**Prerequisites:**
```powershell
dapr init
```

**Run the agent:**
```powershell
dapr run --app-id stateful-llm --app-port 8082 --dapr-http-port 3500 --resources-path components/ -- python durable_agents.py
```

**Test the agent (in another terminal):**
```powershell
# Start a workflow
curl -i -X POST http://localhost:8082/start-workflow -H "Content-Type: application/json" -d "{\"task\": \"I prefer vegetarian food\"}"

# Check workflow status (replace WORKFLOW_ID)
curl -i -X GET http://localhost:3500/v1.0/workflows/dapr/WORKFLOW_ID
```

**Key Points:**
- Persistent memory across sessions
- REST API endpoints for workflow interaction
- Structured recipe suggestions with Pydantic models
- Dapr state store integration

---

## Demo 4: Simple Workflow
**File:** `simple_agent_workflow.py`

This demonstrates multi-step LLM processes with workflow orchestration.

```powershell
dapr run --app-id dapr-agent-wf -- python simple_agent_workflow.py
```

**Key Points:**
- Multi-step workflow with `@workflow` and `@task` decorators
- Each step is durable and can be retried
- Builds learning path from skill input to study schedule
- JSON parsing from LLM responses

---

## Demo 5: Agent with Vector Store
**File:** `simple_agent_vector_store.py`

This shows an agent that can search and store documents using vector embeddings.

**Additional dependencies:**
```powershell
pip install sentence-transformers chromadb 'posthog<6.0.0'
```

**Run the agent:**
```powershell
python simple_agent_vector_store.py
```

**Key Points:**
- Vector store for semantic document search
- Sentence transformers for embeddings
- Tools for searching and adding quotes
- Persistent ChromaDB storage
- Metadata support for structured document storage

---

## Summary
These examples demonstrate the progression from simple LLM calls to sophisticated agent systems:

1. **Basic LLM** - Foundation interaction pattern
2. **Agent + Tools** - Adding custom capabilities
3. **Durable Agent** - Stateful, persistent agents with workflows
4. **Workflows** - Multi-step orchestrated processes
5. **Vector Store** - Semantic search and document management

Each builds on the previous concepts, showing how Dapr Agents enables scalable, production-ready AI applications.
