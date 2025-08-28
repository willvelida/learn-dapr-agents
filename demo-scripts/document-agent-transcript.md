# Dapr Agents Document Chat Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd lessons\document-agent-chainlit
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

**Prerequisites:**
```powershell
# Start Redis for conversation memory
docker run -d --name redis-doc-agent -p 6379:6379 redis

# Initialize Dapr
dapr init
```

---

## Demo: Document Chat Agent
**File:** `app.py`

This demonstrates a complete document analysis application using Chainlit UI and Dapr Agents.

```powershell
dapr run --app-id doc-agent --resources-path .\components\ -- chainlit run .\app.py -w
```

**Open your browser to:** `http://localhost:8000`

**Key Features:**
- **Interactive UI** - Chainlit provides a modern chat interface
- **PDF Upload** - Drag and drop PDF documents for analysis
- **Document Processing** - Unstructured library extracts text and metadata
- **Persistent Memory** - Conversation context preserved with Redis
- **File Storage** - Dapr bindings upload files to cloud storage
- **Document Understanding** - Agent learns from uploaded content

**Demo Flow:**
1. **Upload Document** - Upload a PDF file through the web interface
2. **Document Processing** - Agent extracts and learns from document content
3. **Interactive Chat** - Ask questions about the document content
4. **Memory Persistence** - Conversation context maintained across sessions

**Key Points:**
- `@cl.on_chat_start` - Handles initial file upload and processing
- `@cl.on_message` - Processes user questions about the document
- `partition_pdf()` - Extracts structured text from PDF documents
- `ConversationDaprStateMemory` - Persistent conversation history
- `DaprClient.invoke_binding()` - File upload to cloud storage
- Agent learns document content and answers questions contextually

---

## Component Architecture
The application uses several Dapr components:

**State Store:**
- `conversationmemory.yaml` - Redis for conversation persistence

**Bindings:**
- `filestorage.yaml` - Azure Blob Storage for document uploads

**Libraries:**
- **Chainlit** - Modern chat UI framework
- **Unstructured** - Document processing and text extraction
- **Dapr Agents** - AI agent with memory capabilities

---

## Summary
This demo showcases a production-ready document analysis application:

**Key Capabilities:**
- **Document Upload** - PDF processing with metadata extraction
- **Intelligent Chat** - Context-aware conversations about documents
- **Persistent Memory** - Conversation history across sessions
- **Cloud Storage** - Scalable file storage with Dapr bindings
- **Modern UI** - Professional chat interface with Chainlit

**Use Cases:**
- Document Q&A systems
- Knowledge base exploration
- Research assistance
- Content analysis tools

Perfect example of combining Dapr Agents with modern UI frameworks for real-world applications.
