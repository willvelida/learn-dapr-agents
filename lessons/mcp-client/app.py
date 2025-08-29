import asyncio
import logging
from dotenv import load_dotenv

from dapr_agents import DurableAgent
from dapr_agents.tool.mcp import MCPClient


async def main():
    try:
        # Load MCP tools from server (stdio or sse)
        client = MCPClient()
        await client.connect_sse("local", url="http://localhost:8000/sse")

        # Convert MCP tools to AgentTool list
        tools = client.get_all_tools()

        # Create the Stock Agent using those tools
        stock_agent = DurableAgent(
            role="Stock Agent Assistant",
            name="Stockie",
            goal="Help humans get stock info using smart tools.",
            instructions=[
                "Respond clearly and helpfully to stock-related questions.",
                "Use tools when appropriate to fetch or simulate stock data.",
                "You may sometimes jump after answering the stock question.",
            ],
            tools=tools,
            message_bus_name="messagepubsub",
            state_store_name="workflowstatestore",
            state_key="workflow_state",
            agents_registry_store_name="agentstatestore",
            agents_registry_key="agents_registry",
        ).as_service(port=8001)

        # Start the FastAPI agent service
        await stock_agent.start()

    except Exception as e:
        logging.exception("Error starting stock agent service", exc_info=e)


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())