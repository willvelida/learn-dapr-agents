#!/usr/bin/env python3
"""
Stateful Augmented LLM Pattern: Book Recommender
Demonstrates:
1. Memory - remembering user genre preferences
2. Tool use - accessing book data
3. LLM abstraction
4. Durable execution as a workflow agent
"""

import asyncio
import logging
from typing import List
from pydantic import BaseModel, Field
from dapr_agents import tool, DurableAgent
from dapr_agents.memory import ConversationDaprStateMemory
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
    try:
        book_agent = DurableAgent(
            name="BookBuddy",
            role="Book Recommendation Assistant",
            goal="Help users discover great books and remember their genre preferences",
            instructions=[
                "Remember the user's favorite genres",
                "Use tools to recommend books based on those genres",
                "Provide clear and friendly suggestions"
            ],
            tools=[recommend_books],
            message_bus_name="messagepubsub",
            state_store_name="workflowstatestore",
            state_key="workflow_state",
            agents_registry_store_name="registrystatestore",
            agents_registry_key="agents_registry",
            memory=ConversationDaprStateMemory(
                store_name="conversationstore",
                session_id="book-session-001"
            )
        )

        book_agent.as_service(port=8002)
        await book_agent.start()
        print("BookBuddy Agent is running on port 8002")

    except Exception as e:
        print(f"Error starting BookBuddy service: {e}")

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())