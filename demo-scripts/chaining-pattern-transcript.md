# Chaining Pattern Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd patterns\chaining
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

**Prerequisites:**
```powershell
# Start Redis for workflow state
docker run -d --name redis-chaining -p 6379:6379 redis

# Initialize Dapr
dapr init
```

---

## Demo: Agent Chaining Workflow
**File:** `app.py`

This demonstrates the Chaining pattern - sequential agent collaboration with data flow between stages.

```powershell
dapr run --app-id job-application-chain --resources-path .\components\ -- python app.py
```

**Key Features:**
- **Sequential Processing** - Multi-stage workflow with data dependencies
- **Specialized Agents** - Different agents for resume and cover letter tasks
- **Tool Integration** - Skills matching tool enhances agent capabilities
- **Structured Data Flow** - Pydantic models ensure type-safe data passing

**Workflow Stages:**
1. **Profile Extraction** - Extract user skills and target role
2. **Resume Generation** - Resume agent uses skill-matching tool
3. **Cover Letter Creation** - Cover letter agent uses resume data

**Pattern Benefits:**
- **Specialization** - Each agent focuses on specific expertise
- **Quality Control** - Sequential validation and refinement
- **Reusability** - Agents can be reused in different workflows
- **Maintainability** - Clear separation of concerns

**Use Cases:**
- Content creation pipelines
- Multi-step approval processes
- Document generation workflows
- Complex data transformation tasks

This pattern shows how to build sophisticated workflows by chaining specialized agents together.
