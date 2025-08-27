import asyncio
from stock_tools import get_stock_price
from dapr_agents import Agent
from dotenv import load_dotenv

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
    await StockAgent.run("What are the current prices of AAPL, TSLA, and MSFT?")

if __name__ == "__main__":
    asyncio.run(main())