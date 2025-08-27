from dapr_agents import tool
from pydantic import BaseModel, Field
import random

class GetStockPriceSchema(BaseModel):
    symbol: str = Field(description="Stock ticker symbol to look up")

@tool(args_model=GetStockPriceSchema)
def get_stock_price(symbol: str) -> str:
    """Get current stock price for a given symbol"""
    price = round(random.uniform(100, 500), 2)
    return f"The current price of {symbol.upper()} is ${price}"

tools = [get_stock_price]