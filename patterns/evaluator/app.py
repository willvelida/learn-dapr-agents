#!/usr/bin/env python3
"""
Evaluator-Optimizer Pattern: Recipe Refinement

1. Generator LLM creates or refines a recipe
2. Evaluator LLM scores the recipe and returns feedback
3. Loop until the recipe meets criteria or max iterations reached
"""

import logging
import json
from typing import List
from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr.ext.workflow import DaprWorkflowContext
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Model for evaluation feedback
class Evaluation(BaseModel):
    score: int = Field(..., description="Quality score from 1–10")
    feedback: List[str] = Field(..., description="Concrete suggestions for improvement")
    meets_criteria: bool = Field(..., description="True if recipe satisfies all criteria")

@workflow(name="recipe_refinement_workflow")
def recipe_refinement_workflow(ctx: DaprWorkflowContext, params: dict):
    request        = params["request"]        # e.g. “A healthy vegan breakfast”
    criteria       = params["criteria"]       # e.g. “high protein, low sugar, easy ingredients”
    max_iterations = params.get("max_iterations", 2)

    logging.info("🔄 Generating initial recipe draft…")
    current_recipe: str = yield ctx.call_activity(
        generate_recipe, input={"request": request, "feedback": None}
    )

    iteration = 1
    meets_criteria = False
    evaluation: Evaluation = None

    while iteration <= max_iterations and not meets_criteria:
        logging.info(f"🧐 Evaluating draft (iteration {iteration})…")
        evaluation_result = yield ctx.call_activity(
            evaluate_recipe,
            input={"recipe": current_recipe, "criteria": criteria}
        )
        
        # Handle case where LLM returns dict instead of Pydantic model
        if isinstance(evaluation_result, dict):
            evaluation = Evaluation(**evaluation_result)
        else:
            evaluation = evaluation_result

        logging.info(f"Score: {evaluation.score}/10, Meets criteria: {evaluation.meets_criteria}")
        if evaluation.meets_criteria:
            meets_criteria = True
            break

        logging.info("✍️ Refining recipe based on feedback…")
        current_recipe = yield ctx.call_activity(
            generate_recipe,
            input={"request": request, "feedback": evaluation.feedback}
        )
        iteration += 1

    return {
        "final_recipe": current_recipe,
        "iterations": iteration,
        "final_score": evaluation.score if evaluation else 0
    }

@task(description="""
Create or refine a recipe for: {request}
If feedback is provided, incorporate it into the new version.
""")
def generate_recipe(request: str, feedback: List[str] = None) -> str:
    # Implemented as an LLM prompt under the hood
    pass

@task(description="""
Evaluate the given recipe against these criteria: {criteria}
Return a score, actionable feedback, and a meets_criteria flag.
Recipe: {recipe}
""")
def evaluate_recipe(recipe: str, criteria: str) -> Evaluation:
    # Implemented as an LLM prompt under the hood
    pass

def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    wfapp = WorkflowApp()
    
    params = {
        "request": "A healthy vegan breakfast recipe",
        "criteria": "high protein, low sugar, easy ingredients",
        "max_iterations": 2
    }

    print("\n=== EVALUATOR-OPTIMIZER PATTERN: RECIPE REFINEMENT ===")
    result = wfapp.run_and_monitor_workflow_sync(
        recipe_refinement_workflow, input=params
    )

    # Handle different result types
    if isinstance(result, str):
        try:
            # Try to parse as JSON
            result = json.loads(result)
        except json.JSONDecodeError:
            print("\nWorkflow returned a string that is not valid JSON.")
            print(f"Result content: {result}")
            return

    if result and isinstance(result, dict):
        print("\nFinal Recipe (score: {0}/10 after {1} iterations):\n{2}".format(
            result["final_score"], result["iterations"], result["final_recipe"]
        ))
        print("\nRecipe Refinement completed successfully!")
    else:
        print("\nWorkflow failed to complete.")
        print(f"Result type: {type(result)}")
        print(f"Result content: {result}")
        print("Check logs for errors.")
    
if __name__ == "__main__":
    main()