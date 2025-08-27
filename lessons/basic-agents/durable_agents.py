import asyncio
import logging
from typing import List
from pydantic import BaseModel, Field
from dapr_agents import tool, DurableAgent
from dapr_agents.memory import ConversationDaprStateMemory
from dotenv import load_dotenv

# Define structured output models for recipes
class Recipe(BaseModel):
    name: str = Field(description="Name of the recipe")
    ingredients: List[str] = Field(description="List of ingredients")

# Define input model for tool validation
class PreferenceSchema(BaseModel):
    dietary_preference: str = Field(description="User's dietary preference")

# Create a tool that returns structured recipe data
@tool(args_model=PreferenceSchema)
def suggest_recipes(dietary_preference: str) -> List[Recipe]:
    """Suggest recipes based on dietary preference"""
    if dietary_preference.lower() == "vegetarian":
        return [
            Recipe(name="Veggie Stir Fry", ingredients=["Broccoli", "Carrots", "Tofu"]),
            Recipe(name="Lentil Soup", ingredients=["Lentils", "Tomatoes", "Spinach"])
        ]
    elif dietary_preference.lower() == "keto":
        return [
            Recipe(name="Keto Chicken Salad", ingredients=["Chicken", "Avocado", "Olive Oil"]),
            Recipe(name="Zucchini Noodles", ingredients=["Zucchini", "Parmesan", "Garlic"])
        ]
    else:
        return [
            Recipe(name="Grilled Cheese", ingredients=["Bread", "Cheddar", "Butter"]),
            Recipe(name="Spaghetti Bolognese", ingredients=["Spaghetti", "Beef", "Tomato"])
        ]
    
async def main():
    try:
        # Create a durable agent with persistent memory and workflow capabilities
        chef_agent = DurableAgent(
            name="HealthyChef",
            role="Recipe Assistant",
            goal="Suggest recipes and remember dietary preferences",
            instructions=[
                "Ask for dietary preferences",
                "Suggest recipes based on preferences",
                "Remember what the user likes"
            ],
            tools=[suggest_recipes],
            # Dapr component configurations for persistence
            message_bus_name="messagepubsub",
            state_store_name="workflowstatestore",
            state_key="chef_state",
            agents_registry_store_name="registrystatestore",
            agents_registry_key="chef_registry",
            # Persistent conversation memory
            memory=ConversationDaprStateMemory(
                store_name="conversationstore", session_id="chef-session"
            )
        )

        # Start the agent as a service with REST API endpoints
        chef_agent.as_service(port=8082)
        await chef_agent.start()
        print("HealthyChef Agent is running")
    
    except Exception as e:
        print(f"Error starting service: {e}")

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())