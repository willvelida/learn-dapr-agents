import logging
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr.ext.workflow import DaprWorkflowContext
import random

load_dotenv()
logging.basicConfig(level=logging.INFO)

class Genre(BaseModel):
    name: str = Field(..., description="Movie genre")

class Genres(BaseModel):
    genres: List[Genre] = Field(..., description="List of movie genres")

@workflow(name="movie_night_workflow")
def movie_night_workflow(ctx: DaprWorkflowContext):
    genres: Genres = yield ctx.call_activity(pick_genres)
    parallel_tasks = [ctx.call_activity(recommend_movie, input={"genre": g["name"]}) for g in genres["genres"]]
    recommendations = yield wfapp.when_all(parallel_tasks)
    plan = yield ctx.call_activity(summarize_plan, input={"recommendations": recommendations})
    return plan

@task(description="Pick 3 random movie genres")
def pick_genres() -> Genres:
    options = ["Action", "Comedy", "Sci-Fi", "Drama", "Horror"]
    selected = random.sample(options, 3)
    return Genres(genres=[Genre(name=g) for g in selected])

@task(description="Recommend a movie in the {genre} genre")
def recommend_movie(genre: str) -> str:
    samples = {
        "Action": "Mad Max: Fury Road",
        "Comedy": "The Grand Budapest Hotel",
        "Sci-Fi": "Interstellar",
        "Drama": "The Shawshank Redemption",
        "Horror": "Get Out"
    }
    return f"{genre}: {samples.get(genre, 'Unknown')}"

@task(description="Summarize the movie night plan based on recommendations")
def summarize_plan(recommendations: List[str]) -> str:
    return "🎥 Movie Night Picks:\n" + "\n".join(recommendations)

if __name__ == "__main__":
    wfapp = WorkflowApp()
    logging.info("Planning your movie night...")
    result = wfapp.run_and_monitor_workflow_sync(movie_night_workflow)
    logging.info(f"\n{result}")