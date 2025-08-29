from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("TestStockServer")

@mcp.tool()
def get_stock_price(symbol: str) -> str:
    """Get current stock price for a given symbol"""
    price = round(random.uniform(100, 500), 2)
    return f"The current price of {symbol.upper()} is ${price}"