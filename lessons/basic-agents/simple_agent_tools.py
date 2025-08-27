import asyncio
from dapr_agents import tool, Agent
from dotenv import load_dotenv

load_dotenv()

# Define a custom tool for the agent
@tool
def get_stock_price() -> str:
    """Get current stock price of Velocity Inc"""
    return "VELO PRICE IS $650 USD"

async def main():
    # Create an agent with the custom tool
    stock_agent = Agent(
        name="StockAgent",
        role="Stock Assistant",
        instructions=["Help users with stock information"],
        tools=[get_stock_price]  # Provide the tool to the agent
    )

    # Run the agent with a user query
    response = await stock_agent.run("What's the current stock price of Velocity Inc?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())