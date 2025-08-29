# Evaluator Pattern Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd patterns\evaluator
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

**Prerequisites:**
```powershell
# Start Redis for workflow state
docker run -d --name redis-evaluator -p 6379:6379 redis

# Initialize Dapr
dapr init
```

---

## Demo: Evaluator-Optimizer Pattern
**File:** `app.py`

This demonstrates the Evaluator-Optimizer pattern - iterative refinement using separate generation and evaluation agents.

```powershell
dapr run --app-id evaluator-optimizer --resources-path .\components\ -- python app.py
```

**Key Features:**
- **Iterative Refinement** - Generate, evaluate, improve cycle
- **Quality Control** - Dedicated evaluator provides structured feedback
- **Convergence Logic** - Loop until criteria met or max iterations reached
- **Structured Evaluation** - Pydantic models for consistent feedback format

**Workflow Stages:**
1. **Initial Generation** - Create first recipe draft
2. **Evaluation Loop** - Score and provide feedback
3. **Refinement** - Improve based on evaluation feedback
4. **Convergence** - Stop when criteria met or max iterations

**Pattern Benefits:**
- **Quality Assurance** - Systematic evaluation and improvement
- **Objective Assessment** - Separate evaluator reduces bias
- **Measurable Progress** - Scoring tracks improvement over iterations
- **Flexible Criteria** - Configurable evaluation standards

**Use Cases:**
- Content quality improvement
- Code review automation
- Creative writing refinement
- Product design optimization
- Training data generation

This pattern shows how to achieve high-quality outputs through systematic evaluation and iterative improvement.
