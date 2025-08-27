# Dapr Agents LLM Workflows Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd lessons\llm-workflows
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

**Prerequisites:**
```powershell
# Start Redis for workflow state storage
docker run -d --name redis-workflow -p 6379:6379 redis

# Initialize Dapr
dapr init
```

---

## Demo 1: Recipe Builder Workflow
**File:** `recipe_builder.py`

This demonstrates a simple multi-step workflow with structured data flow between tasks.

```powershell
dapr run --app-id recipe-builder --resources-path .\components\ -- python recipe_builder.py
```

**Key Points:**
- `@workflow` decorator for orchestrating multi-step processes
- `@task` decorators for individual workflow steps
- Pydantic models for structured data passing between tasks
- `WorkflowApp` with OpenAI LLM integration
- Sequential task execution with data dependencies
- Durable workflow state management

---

## Demo 2: Movie Night Planner Workflow
**File:** `movie_night_planner.py`

This shows advanced workflow patterns with parallel execution and complex orchestration.

```powershell
dapr run --app-id movie-planner --resources-path .\components\ -- python movie_night_planner.py
```

**Key Points:**
- Parallel task execution with `when_all()`
- Complex Pydantic models with nested structures
- Random data generation for demonstration
- Multi-step workflow with fan-out/fan-in pattern
- Workflow monitoring and result aggregation
- Production-ready workflow orchestration

---

## Workflow Architecture
The examples demonstrate key workflow concepts:

**Workflow Components:**
- `workflowstate.yaml` - Redis state store for workflow persistence
- `@workflow` - Main orchestration function
- `@task` - Individual executable steps
- `DaprWorkflowContext` - Workflow execution context

**Execution Patterns:**
- **Sequential** - Tasks execute one after another
- **Parallel** - Multiple tasks execute simultaneously
- **Fan-out/Fan-in** - Split work, then aggregate results

---

## Summary
These workflows demonstrate the progression from simple to complex orchestration:

1. **Recipe Builder** - Sequential workflow with structured data flow
2. **Movie Planner** - Parallel execution with result aggregation

Key benefits:
- **Durability** - Workflows survive failures and restarts
- **Scalability** - Parallel task execution
- **Type Safety** - Pydantic models ensure data consistency
- **Monitoring** - Built-in workflow state tracking
- **LLM Integration** - Seamless AI model integration

Perfect foundation for building complex, durable AI applications with Dapr Agents.
