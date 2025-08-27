import asyncio
from stock_tools import get_stock_price
from dapr_agents import Agent
from dotenv import load_dotenv

from phoenix.otel import register
from dapr_agents.observability import DaprAgentsInstrumentor

load_dotenv()

tools = [get_stock_price]

StockAgent = Agent(
    name="Stockie",
    role="Stock Market Assistant",
    goal="Assist with stock-related questions and actions",
    instructions=[
        "Always answer the user's main stock question directly and clearly.",
        "If you perform any additional actions (like jumping), summarize those actions and their results.",
        "At the end, provide a concise summary that combines all stock information and any other actions you performed.",
    ],
    tools=tools
)

async def main():
    # Register Dapr Agents with Phoenix OpenTelemetry
    tracer_provider = register(
        project_name="dapr-stock-agent",
        protocol="http/protobuf"
    )

    # Initialize Dapr Agents OpenTelemetry instrumentor
    instrumentor = DaprAgentsInstrumentor()
    instrumentor.instrument(tracer_provider=tracer_provider, skip_dep_check=True)

    await StockAgent.run("What are the current prices of AAPL, TSLA, and MSFT?")

if __name__ == "__main__":
    asyncio.run(main())