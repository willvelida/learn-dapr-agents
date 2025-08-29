import asyncio
import logging
from typing import List
from pydantic import BaseModel, Field
from dapr_agents import tool, Agent
from dotenv import load_dotenv

# Define tool output model
class BookRecommendation(BaseModel):
    title: str = Field(description="Book title")
    author: str = Field(description="Author name")

# Define tool input model
class GenreSchema(BaseModel):
    genre: str = Field(description="Preferred book genre")

# Define book recommendation tool
@tool(args_model=GenreSchema)
def recommend_books(genre: str) -> List[BookRecommendation]:
    """Recommend books based on genre."""
    mock_db = {
        "sci-fi": [
            BookRecommendation(title="Dune", author="Frank Herbert"),
            BookRecommendation(title="Neuromancer", author="William Gibson")
        ],
        "fantasy": [
            BookRecommendation(title="The Name of the Wind", author="Patrick Rothfuss"),
            BookRecommendation(title="Mistborn", author="Brandon Sanderson")
        ],
        "mystery": [
            BookRecommendation(title="Gone Girl", author="Gillian Flynn"),
            BookRecommendation(title="The Girl with the Dragon Tattoo", author="Stieg Larsson")
        ]
    }
    return mock_db.get(genre.lower(), [])

async def main():
    book_agent = Agent(
        name="BookBuddy",
        role="Book Recommendation Assistant",
        instructions=["Remember user genre preferences and suggest books accordingly."],
        tools=[recommend_books]
    )

    print("\n--- First interaction ---")
    await book_agent.run("I love fantasy novels")

    print("\n--- Second interaction (uses memory and tool) ---")
    await book_agent.run("Can you recommend something to read?")

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())