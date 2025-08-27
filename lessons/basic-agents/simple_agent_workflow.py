from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr.ext.workflow import DaprWorkflowContext
from dapr_agents.llm import OpenAIChatClient
from dotenv import load_dotenv
import json
import re

load_dotenv()

def parse_json_from_response(response: str):
    """Extract and parse JSON from LLM response that may contain markdown"""
    # Try to find JSON in markdown code blocks
    json_match = re.search(r'```(?:json)?\s*(\[.*?\]|\{.*?\})\s*```', response, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # If no markdown blocks, try to find JSON directly
        json_match = re.search(r'(\[.*?\]|\{.*?\})', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Fallback: assume the entire response is JSON
            json_str = response.strip()
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # If parsing fails, return the original response
        return response

# Each task represents a step in the workflow
@task(description="Break down {skill} into a JSON list of subtopics. Return ONLY a JSON array of strings, no other text.")
def identify_subtopics(skill: str) -> str:
    """Return a JSON string that can be parsed into a list"""
    pass

@task(description="Find learning resources for each subtopic: {subtopics}. Return ONLY a JSON object with subtopic names as keys and URLs as values.")
def find_resources(subtopics: str) -> str:
    """Return a JSON string that can be parsed into a dict"""
    pass

@task(description="Create a weekly study schedule for resources: {resources}. Return ONLY a JSON object with week numbers as keys and topics as values.")
def create_schedule(resources: str) -> str:
    """Return a JSON string that can be parsed into a dict"""
    pass

# Define the workflow that chains tasks together
@workflow(name="build_learning_path")
def build_learning_path(ctx: DaprWorkflowContext, skill: str):
    # Step 1: Identify subtopics
    subtopics_response = yield ctx.call_activity(identify_subtopics, input=skill)
    subtopics = parse_json_from_response(subtopics_response)

    # Step 2: Find resources for each subtopic (pass as JSON string)
    resources_response = yield ctx.call_activity(find_resources, input=json.dumps(subtopics))
    resources = parse_json_from_response(resources_response)

    # Step 3: Create a study schedule (pass as JSON string)
    schedule_response = yield ctx.call_activity(create_schedule, input=json.dumps(resources))
    schedule = parse_json_from_response(schedule_response)

    return schedule

if __name__ == '__main__':
    # Create and run the workflow application
    wfapp = WorkflowApp(llm=OpenAIChatClient())

    # Execute the workflow synchronously and monitor progress
    result = wfapp.run_and_monitor_workflow_sync(
        build_learning_path,
        input="Python"
    )
    print(f"Learning Path Result: {result}")