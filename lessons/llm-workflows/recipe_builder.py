from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr.ext.workflow import DaprWorkflowContext
from dapr_agents.llm import OpenAIChatClient
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import random

load_dotenv()

# Define Pydantic models for structured responses
class Ingredients(BaseModel):
    items: List[str]

# Define workflow logic
@workflow(name="recipe_builder_workflow")
def recipe_builder_workflow(ctx: DaprWorkflowContext):
    dish = yield ctx.call_activity(pick_dish)
    ingredients = yield ctx.call_activity(get_ingredients, input={"dish": dish})
    recipe = yield ctx.call_activity(summarize_recipe, input={"dish": dish, "ingredients": ingredients})
    return recipe

@task(description="Pick a random dish type to prepare")
def pick_dish() -> str:
    return random.choice(["pasta", "salad", "stir-fry"])

@task(description="Get ingredients for a {dish}")
def get_ingredients(dish: str) -> Ingredients:
    options = {
        "pasta": ["spaghetti", "tomato sauce", "garlic"],
        "salad": ["lettuce", "tomato", "feta cheese"],
        "stir-fry": ["chicken", "broccoli", "soy sauce"]
    }
    return Ingredients(items=options.get(dish, []))

@task(description="Summarize the recipe for {dish} with given ingredients")
def summarize_recipe(dish: str, ingredients: Ingredients) -> str:
    return f"To make {dish}, you'll need: {', '.join(ingredients.items)}."

if __name__ == '__main__':
    wfapp = WorkflowApp(llm=OpenAIChatClient())
    result = wfapp.run_and_monitor_workflow_sync(recipe_builder_workflow)
    print(f"Recipe: {result}")

