import asyncio
from stock_tools import get_stock_price
from dapr_agents import Agent
from dotenv import load_dotenv
from dapr_agents.memory import ConversationDaprStateMemory

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
    memory=ConversationDaprStateMemory(store_name="stockstore",session_id="stock-id"),
    tools=tools
)

async def main():
    await StockAgent.run("What are the current prices of AAPL, TSLA, and MSFT?")
    print(StockAgent.chat_history)

    await StockAgent.run("What was the stock price for MSFT again?")
    print(StockAgent.chat_history)

    StockAgent.reset_memory()
    print("Chat history after reset:")
    print(StockAgent.chat_history)

if __name__ == "__main__":
    asyncio.run(main())