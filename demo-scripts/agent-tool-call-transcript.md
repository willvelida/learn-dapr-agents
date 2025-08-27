# Dapr Agents with Tools Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd lessons\agent-tool-call
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

---

## Demo 1: Stock Tools Foundation
**File:** `stock_tools.py`

This demonstrates creating custom tools with Pydantic validation for agents.

**Key Points:**
- `@tool` decorator with `args_model` for type safety
- Pydantic schema validation for tool parameters
- Mock stock price generation for demonstration
- Foundation for all agent tool interactions

---

## Demo 2: Basic Agent with Tools
**File:** `stock_agent.py`

This shows how to create an agent that can use custom tools.

```powershell
python stock_agent.py
```

**Key Points:**
- `Agent` class with custom tools integration
- Clear role, goal, and instructions definition
- Tool execution within agent context
- Async agent execution pattern

---

## Demo 3: Agent with Memory
**File:** `stock_agent_memory.py`

This demonstrates adding persistent memory to agents using Dapr state stores.

**Prerequisites:**
```powershell
# Start Redis for state storage
docker run -d --name redis-agent -p 6379:6379 redis

# Initialize Dapr
dapr init
```

**Run the agent:**
```powershell
dapr run --app-id stockagent --resources-path .\components\ -- python stock_agent_memory.py
```

**Key Points:**
- `ConversationDaprStateMemory` for persistent conversations
- State store integration with Redis
- Session-based memory management
- Conversation context preservation across runs

---

## Demo 4: Agent with Observability
**File:** `stock_agent_observability.py`

This shows how to add monitoring and tracing to your agents.

**Prerequisites:**
```powershell
# Start Phoenix observability platform
docker-compose up -d phoenix
```

**Run the agent:**
```powershell
python stock_agent_observability.py
```

**Access observability dashboard:**
Open browser to `http://localhost:6006`

**Key Points:**
- Phoenix OpenTelemetry integration
- `DaprAgentsInstrumentor` for automatic tracing
- Real-time monitoring of agent interactions
- Performance and debugging insights

---

## Demo 5: Durable Agent
**File:** `durable_stock_agent.py`

This demonstrates workflow-based agents with full durability and state management.

**Run the durable agent:**
```powershell
dapr run --app-id durablestockagent --resources-path .\components\ -- python durable_stock_agent.py
```

**Key Points:**
- `DurableAgent` with workflow capabilities
- Message bus integration for communication
- Multiple state stores for different purposes
- Production-ready agent architecture

---

## Demo 6: Durable Agent with Observability
**File:** `durable_stock_agent_observability.py`

This combines durability with full observability for production monitoring.

**Prerequisites:**
```powershell
# Ensure Phoenix is running
docker-compose up -d phoenix
```

**Run the complete solution:**
```powershell
dapr run --app-id durablestockagent --resources-path .\components\ -- python durable_stock_agent_observability.py
```

**Key Points:**
- Full production setup with durability and observability
- Combined workflow management and monitoring
- Enterprise-ready agent deployment
- Complete tracing and performance metrics

---

## Component Architecture
The examples use several Dapr components:

**State Stores:**
- `statestore.yaml` - Agent registry and workflow state
- `stockstore.yaml` - Conversation memory storage

**Pub/Sub:**
- `pubsub.yaml` - Message bus for agent communication

**Observability:**
- `docker-compose.yml` - Phoenix platform for monitoring

---

## Summary
This progression demonstrates building production-ready agents:

1. **Custom Tools** - Foundation with type-safe tool creation
2. **Basic Agent** - Simple agent-tool integration
3. **Memory Integration** - Persistent conversation context
4. **Observability** - Monitoring and performance tracking
5. **Durable Workflows** - Production-ready agent architecture
6. **Complete Solution** - Enterprise deployment with full observability

Each step builds toward a scalable, monitored, and durable agent system suitable for production use.
