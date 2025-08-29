import logging
from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr_agents.llm import OpenAIChatClient
from dapr.ext.workflow import DaprWorkflowContext
from dapr_agents import tool, Agent
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

# Define structured output models
class UserProfile(BaseModel):
    role: str = Field(description="Target job role")
    skills: List[str] = Field(description="List of user skills")
    goal: str = Field(description="Career goal or objective")

class ResumeOutline(BaseModel):
    summary: str = Field(description="Professional summary")
    skills: List[str] = Field(description="Relevant skills")
    experience: List[str] = Field(description="Experience highlights")

class SkillMatchSchema(BaseModel):
    role: str = Field(description="Target job role")
    skills: List[str] = Field(description="List of user skills")

@tool(args_model=SkillMatchSchema)
def match_skills(role: str, skills: List[str]) -> List[str]:
    """Match user skills to role requirements."""
    role_requirements = {
        "software engineer": ["Python", "JavaScript", "Git", "Cloud", "Teamwork"],
        "full stack developer": ["JavaScript", "HTML/CSS", "React", "Node.js", "Python", "Git"],
        "data analyst": ["SQL", "Excel", "Visualization", "Statistics", "Python"]
    }
    # Get requirements for the role (case insensitive)
    reqs = role_requirements.get(role.lower(), [])
    # Find skills that match requirements (case insensitive)
    matched = []
    for skill in skills:
        for req in reqs:
            if skill.lower() in req.lower() or req.lower() in skill.lower():
                matched.append(skill)
                break
    return matched

resume_agent = Agent(
    name="ResumeAgent",
    role="Resume Builder",
    goal="Create a resume outline from user profile and skills",
    instructions=[
        "Use the match_skills tool to align user skills with role requirements",
        "Structure the resume into sections: Summary, Skills, Experience"
    ],
    tools=[match_skills]
)

cover_letter_agent = Agent(
    name="CoverLetterAgent",
    role="Cover Letter Writer",
    goal="Write a personalized cover letter from a resume outline",
    instructions=[
        "Use the resume outline to craft a compelling narrative",
        "Highlight strengths and express enthusiasm for the role"
    ]
)

@workflow(name="job_application_workflow")
def job_application_workflow(ctx: DaprWorkflowContext, user_input: str):
    # 1) Extract structured user profile
    profile = yield ctx.call_activity(extract_user_profile, input=user_input)
    logging.info("Step 1 – Extracted Profile:\n%s", profile)

    # 2) Generate resume outline (uses resume_agent + match_skills tool)
    # Convert profile to dict for proper task input handling
    profile_dict = profile.model_dump() if hasattr(profile, 'model_dump') else profile
    resume_result = yield ctx.call_activity(generate_resume_outline, input=profile_dict)
    
    # Extract content from agent response if it's a dict
    resume_info = resume_result.get('content', resume_result) if isinstance(resume_result, dict) else resume_result
    logging.info("Step 2 – Resume Info:\n%s", resume_info)

    # 3) Write cover letter (uses cover_letter_agent)
    letter_result = yield ctx.call_activity(write_cover_letter, input={"resume_info": resume_info})
    
    # Extract content from agent response if it's a dict
    letter = letter_result.get('content', letter_result) if isinstance(letter_result, dict) else letter_result
    logging.info("Step 3 – Cover Letter:\n%s", letter)

    return letter

@task(description="Extract the user's target role and relevant skills from the provided input.")
def extract_user_profile(user_input: str) -> UserProfile:
    # Implementation is handled by the LLM (prompt‐based)
    pass

@task(agent=resume_agent, description="Generate a resume outline based on the user profile with role: {role}, skills: {skills}, and goal: {goal}. Use the match_skills tool to align skills with the role. Return a clear summary, list of relevant skills, and experience highlights.")
def generate_resume_outline(role: str, skills: List[str], goal: str):
    # No return type annotation to avoid validation issues with agent responses
    pass

@task(agent=cover_letter_agent, description="Write a personalized cover letter based on the resume information: {resume_info}. Make it enthusiastic, concise, and role-focused.")
def write_cover_letter(resume_info: str):
    # No return type annotation to avoid validation issues with agent responses
    pass

def main():
    # Create WorkflowApp with LLM client
    wfapp = WorkflowApp(llm=OpenAIChatClient())
    
    logging.info("Starting job application workflow...")
    
    # Define user input
    user_input = (
        "I'm applying for a software engineering role. "
        "I have experience in Python, cloud infrastructure, and team leadership."
    )
    
    # Run the workflow
    result = wfapp.run_and_monitor_workflow_sync(job_application_workflow, user_input)
    print("\n=== Final Cover Letter ===\n")
    print(result)

if __name__ == "__main__":
    main()