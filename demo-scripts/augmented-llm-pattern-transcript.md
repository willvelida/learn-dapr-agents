# Augmented LLM Pattern Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd patterns\augmented-llm
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

---

## Demo: Augmented LLM with Tools
**File:** `app.py`

This demonstrates the Augmented LLM pattern - combining language models with external tools and memory.

```powershell
python app.py
```

**Key Features:**
- **Tool Integration** - `@tool` decorator for book recommendations
- **Structured Data** - Pydantic models for type-safe tool outputs
- **Memory Capability** - Agent remembers user preferences
- **LLM Enhancement** - External tools augment language model capabilities

**Pattern Benefits:**
- **Enhanced Accuracy** - Tools provide factual, up-to-date information
- **Structured Responses** - Type-safe data exchange between LLM and tools
- **Context Awareness** - Memory enables personalized interactions
- **Extensibility** - Easy to add new tools and capabilities

**Demo Flow:**
1. **First Interaction** - User expresses genre preference (fantasy)
2. **Memory Storage** - Agent remembers the preference
3. **Second Interaction** - Agent uses memory + tool for recommendations
4. **Tool Execution** - `recommend_books` tool provides structured data

**Use Cases:**
- Personal assistants with external data access
- E-commerce recommendation systems
- Customer support with knowledge bases
- Research assistants with specialized tools

This pattern shows how to make LLMs more powerful by combining them with tools and persistent memory.
