#!/usr/bin/env python3
"""
Orchestrator-Workers Pattern: Conference Planner

1. Central orchestrator analyzes the request and creates subtasks
2. Each subtask is delegated to a worker LLM
3. Synthesizer LLM merges all worker outputs into a final conference plan
"""

import logging
from typing import List, Dict, Any

from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr.ext.workflow import DaprWorkflowContext
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

# 1) Models for orchestration
class ConferenceTask(BaseModel):
    task_id: str = Field(..., description="Unique ID for this task")
    description: str = Field(..., description="What this worker should do")
    query: str = Field(..., description="Prompt for the worker LLM")

class OrchestratorPlan(BaseModel):
    tasks: List[ConferenceTask] = Field(..., description="List of subtasks")

# 2) Workflow definition
@workflow(name="conference_planning_workflow")
def conference_planning_workflow(ctx: DaprWorkflowContext, params: dict):
    request = params.get("request")
    logging.info(f"Orchestrator received request:\n{request}")

    # Step 1: Orchestrator creates a task list
    plan_result = yield ctx.call_activity(
        create_plan,
        input={"request": request}
    )
    
    # Handle case where LLM returns dict instead of OrchestratorPlan object
    if isinstance(plan_result, dict):
        plan = OrchestratorPlan(**plan_result)
    else:
        plan = plan_result
        
    logging.info(f"Orchestrator generated {len(plan.tasks)} subtasks")

    # Step 2: Dispatch each subtask to a worker LLM
    worker_outputs: List[Dict[str, Any]] = []
    for task in plan.tasks:
        logging.info(f"→ Dispatching task {task.task_id}: {task.description}")
        result: str = yield ctx.call_activity(
            execute_task,
            input={"task": task.model_dump()}
        )
        worker_outputs.append({"task_id": task.task_id, "result": result})

    # Step 3: Synthesize all worker results into one conference plan
    final_plan: str = yield ctx.call_activity(
        synthesize_plan,
        input={
            "request": request,
            "results": worker_outputs
        }
    )
    logging.info("Orchestrator-Workers flow complete!")
    return final_plan

# 3) Tasks

@task(description="""
Analyze this conference request and break it into subtasks.
Return an OrchestratorPlan containing tasks with:
- task_id
- description
- query
Request: {request}
""")
def create_plan(request: str) -> OrchestratorPlan:
    # Implemented via LLM prompt under the hood
    pass

@task(description="Execute this specific subtask for the conference: {task}")
def execute_task(task: Dict[str, Any]) -> str:
    # Worker LLM processes one piece (venue, speakers, or schedule)
    pass

@task(description="""
Combine these subtask results into a single, well-structured conference plan
Original request: {request}
Sub-results: {results}
""")
def synthesize_plan(request: str, results: List[Dict[str, Any]]) -> str:
    # Synthesizer LLM merges everything into a final plan
    pass

# 4) Kick off the workflow
def main():
    wfapp = WorkflowApp()

    complex_request = """
    Plan a 2-day tech conference in San Francisco.
    We need:
    - A venue for 200 attendees
    - Keynote and panel speakers on AI and Cloud
    - A detailed day-by-day schedule
    Budget is moderate, focus on an educational yet fun experience.
    """

    print("\n=== ORCHESTRATOR-WORKERS PATTERN: CONFERENCE PLANNER ===")
    print(f"\nRequest:\n{complex_request}")

    final_plan = wfapp.run_and_monitor_workflow_sync(
        conference_planning_workflow,
        input={"request": complex_request}
    )

    print("\n=== FINAL CONFERENCE PLAN ===")
    print(final_plan)

if __name__ == "__main__":
    main()