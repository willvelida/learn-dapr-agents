# Routing Pattern Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd patterns\routing
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

**Prerequisites:**
```powershell
# Start Redis for workflow state
docker run -d --name redis-routing -p 6379:6379 redis

# Initialize Dapr
dapr init
```

---

## Demo: Routing Pattern
**File:** `app.py`

This demonstrates the Routing pattern - intelligent classification and delegation to specialized handlers.

```powershell
dapr run --app-id it-support-router --resources-path .\components\ -- python app.py
```

**Key Features:**
- **Intelligent Classification** - Router analyzes and categorizes requests
- **Specialized Handlers** - Different agents for hardware, software, network issues
- **Structured Decision Making** - Pydantic models for routing decisions
- **Batch Processing** - Handle multiple tickets efficiently

**Workflow Stages:**
1. **Classification** - Router analyzes each support ticket
2. **Routing Decision** - Determine appropriate specialist handler
3. **Specialized Handling** - Delegate to domain-specific agent
4. **Response Generation** - Handler provides tailored solution

**Pattern Benefits:**
- **Accuracy** - Specialized agents provide domain-specific expertise
- **Efficiency** - Automatic routing reduces manual triage
- **Scalability** - Easy to add new categories and handlers
- **Consistency** - Structured routing ensures proper handling

**Use Cases:**
- Customer support ticket routing
- Email classification and response
- Document processing workflows
- Multi-channel content moderation
- Automated helpdesk systems

This pattern shows how to build intelligent routing systems that automatically direct requests to the most appropriate specialized handler.
