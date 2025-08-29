# Dapr Agents MCP Integration Demo Transcript

## Setup
First, let's set up our environment:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
cd lessons\mcp-client
pip install -r requirements.txt
```

Make sure you have a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

**Prerequisites:**
```powershell
# Start Redis for state storage
docker run -d --name redis-mcp -p 6379:6379 redis

# Initialize Dapr
dapr init
```

---

## Demo 1: MCP Tools Definition
**File:** `tools.py`

This demonstrates creating tools using the Model Context Protocol (MCP) with FastMCP.

**Key Points:**
- `FastMCP` server for tool definition
- `@mcp.tool()` decorator for MCP-compatible tools
- Simple stock price tool implementation
- Foundation for MCP server integration

---

## Demo 2: MCP Server
**File:** `server.py`

This shows how to run an MCP server that exposes tools over SSE (Server-Sent Events).

```powershell
# Terminal 1: Start MCP Server
python server.py --server_type sse --port 8000
```

**Key Points:**
- **SSE Transport** - Server-Sent Events for real-time communication
- **Starlette Framework** - ASGI web server for MCP endpoints
- **Multiple Transport Types** - Supports both stdio and SSE
- **Tool Exposure** - Makes tools available to MCP clients
- **Production Ready** - Scalable server architecture

---

## Demo 3: Dapr Agent with MCP Client
**File:** `app.py`

This demonstrates a Dapr Agent that consumes tools from an MCP server.

```powershell
# Terminal 2: Start Dapr Agent with MCP Client
dapr run --app-id stockappmcp --app-port 8001 --dapr-http-port 3500 --resources-path .\components\ -- python app.py
```

**Test the integration:**
```powershell
# Terminal 3: Test the agent
curl -X POST http://localhost:8001/start-workflow -H "Content-Type: application/json" -d "{\"task\": \"What is current stock value for Microsoft\"}"
```

**Key Points:**
- **MCPClient** - Connects to MCP server via SSE
- **Tool Integration** - Automatically converts MCP tools to agent tools
- **DurableAgent** - Full workflow capabilities with MCP tools
- **REST API** - FastAPI endpoints for agent interaction
- **Seamless Integration** - MCP tools work like native agent tools

---

## MCP Architecture
The Model Context Protocol enables tool sharing between different AI systems:

**Components:**
- **MCP Server** - Exposes tools via standardized protocol
- **MCP Client** - Consumes tools from MCP servers
- **Transport Layer** - SSE for real-time communication
- **Tool Registry** - Automatic tool discovery and integration

**Benefits:**
- **Interoperability** - Tools work across different AI frameworks
- **Modularity** - Separate tool development from agent logic
- **Scalability** - Distributed tool architecture
- **Reusability** - Share tools between multiple agents

---

## Summary
This demo showcases advanced tool integration using the Model Context Protocol:

**Key Capabilities:**
- **Tool Standardization** - MCP protocol for universal tool sharing
- **Real-time Communication** - SSE transport for live tool execution
- **Agent Integration** - Seamless MCP tool consumption in Dapr Agents
- **Distributed Architecture** - Tools and agents can run separately
- **Production Scalability** - Multiple agents can share the same tool server

**Use Cases:**
- **Microservices Architecture** - Separate tool services from agent logic
- **Tool Marketplaces** - Shared tool ecosystems
- **Multi-Agent Systems** - Common tool infrastructure
- **Enterprise Integration** - Standardized tool interfaces

Perfect example of building scalable, interoperable AI systems with industry-standard protocols.
