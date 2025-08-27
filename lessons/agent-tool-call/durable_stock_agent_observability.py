from dapr_agents import DurableAgent
from dotenv import load_dotenv
from stock_tools import tools
import asyncio
import logging

from phoenix.otel import register
from dapr_agents.observability import DaprAgentsInstrumentor

load_dotenv()

async def main():
    logging.basicConfig(level=logging.INFO)

    # Register OpenTelemetry tracer provider
    tracer_provider = register(
        project_name="dapr-agentic-stock-workflow",
        protocol="http/protobuf"
    )

    # Initialize Dapr Agents Observability Instrumentor
    instrumentor = DaprAgentsInstrumentor()
    instrumentor.instrument(tracer_provider=tracer_provider, skip_dep_check=True)

    stock_agent = DurableAgent(
        name="Stockie",
        role="Stock Market Assistant",
        goal="Assist with stock-related questions and actions",
        instructions=[
            "Always answer the user's main stock question directly and clearly.",
            "If you perform any additional actions (like jumping), summarize those actions and their results.",
            "At the end, provide a concise summary that combines all stock information and any other actions you performed.",
        ],
        message_bus_name="messagepubsub",
        state_store_name="workflowstatestore",
        state_key="workflow_state",
        agents_registry_store_name="agentstatestore",
        agents_registry_key="agents_registry",
        tools=tools
    )

    result = await stock_agent.run("What are the current prices of AAPL, TSLA, and MSFT?")

    print(f"\n Final Result: {result}")

    return result

if __name__ == "__main__":
    asyncio.run(main())