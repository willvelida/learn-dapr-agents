#!/usr/bin/env python3
import logging
import sys
from enum import Enum
from typing import Optional

from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr.ext.workflow import DaprWorkflowContext
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# configure a console logger
console = logging.getLogger("console")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
console.setLevel(logging.INFO)
console.addHandler(handler)
console.propagate = False

# 1) Define the query categories
class QueryType(str, Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK  = "network"
    OTHER    = "other"

# 2) Input and routing models
class SupportQuery(BaseModel):
    query: str = Field(..., description="The user's support ticket text")

class RoutingDecision(BaseModel):
    query_type: QueryType = Field(..., description="Where to route this ticket")
    reason:     str      = Field(..., description="Why it was classified this way")

# 3) Workflow definition
@workflow(name="it_support_batch_workflow")
def it_support_batch_workflow(ctx: DaprWorkflowContext, tickets: list):
    results = []
    
    for idx, user_query in enumerate(tickets, start=1):
        console.info(f"\n--- Processing Ticket #{idx} ---")
        console.info(f"Received ticket: {user_query}")

        # Route the ticket
        decision_response = yield ctx.call_activity(
            route_query,
            input={"query": user_query}
        )
        
        # Extract from response content if it's a response object
        if hasattr(decision_response, 'content'):
            decision_data = decision_response.content
        else:
            decision_data = decision_response
        
        # Create RoutingDecision from the data
        decision = RoutingDecision(**decision_data)
        qtype = decision.query_type
        console.info(f"Classified as: {qtype} ({decision.reason})")

        # Dispatch to the right handler
        if qtype == QueryType.HARDWARE:
            handler_response = yield ctx.call_activity(handle_hardware, input={"query": user_query})
        elif qtype == QueryType.SOFTWARE:
            handler_response = yield ctx.call_activity(handle_software, input={"query": user_query})
        elif qtype == QueryType.NETWORK:
            handler_response = yield ctx.call_activity(handle_network, input={"query": user_query})
        else:
            handler_response = yield ctx.call_activity(handle_other, input={"query": user_query})
        
        # Extract response content
        if hasattr(handler_response, 'content'):
            resp = handler_response.content
        else:
            resp = handler_response

        # print to console for visibility
        print("\n" + "*" * 60)
        print(f"TICKET #{idx} RESPONSE ({qtype.upper()}):")
        print(resp)
        print("*" * 60 + "\n")

        results.append({
            "ticket_number": idx,
            "query": user_query,
            "type": qtype.value,
            "response": resp
        })

    return results

# 4) Tasks

@task(description="""
Classify this support ticket into one of: hardware, software, network, or other.
Explain your reasoning briefly.
Ticket: {query}
""")
def route_query(query: str) -> RoutingDecision:
    pass  # implemented by the LLM

@task(description="Provide hardware troubleshooting steps for: {query}")
def handle_hardware(query: str) -> str:
    pass  # implemented by the LLM

@task(description="Provide software troubleshooting steps for: {query}")
def handle_software(query: str) -> str:
    pass  # implemented by the LLM

@task(description="Provide network troubleshooting steps for: {query}")
def handle_network(query: str) -> str:
    pass  # implemented by the LLM

@task(description="Handle general inquiries or escalate: {query}")
def handle_other(query: str) -> str:
    pass  # implemented by the LLM

# 5) Run through a handful of sample tickets
def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    wfapp = WorkflowApp()

    sample_tickets = [
        "My laptop won’t power on after the update.",
        "The CRM app crashes whenever I click Save.",
        "I cannot reach the corporate VPN from home.",
        "How do I change my VPN password?"
    ]

    console.info("Starting IT Support Ticket Processing...")
    
    # Process all tickets in a single workflow execution
    results = wfapp.run_and_monitor_workflow_sync(
        it_support_batch_workflow,
        input=sample_tickets
    )

if __name__ == "__main__":
    main()