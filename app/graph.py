
from langgraph.graph import StateGraph, START, END

from app.state import JobApplicationState

from app.agents.job_analyst import job_analyst
from app.agents.resume_evaluator import resume_evaluator
from app.agents.skill_gap import skill_gap_agent
from app.agents.application_writer import application_writer
from app.agents.quality_reviewer import quality_reviewer


# Create the graph
builder = StateGraph(JobApplicationState)

# Add all five agents
builder.add_node("job_analyst", job_analyst)
builder.add_node("resume_evaluator", resume_evaluator)
builder.add_node("skill_gap", skill_gap_agent)
builder.add_node("application_writer", application_writer)
builder.add_node("quality_reviewer", quality_reviewer)

# Connect the agents
builder.add_edge(START, "job_analyst")
builder.add_edge("job_analyst", "resume_evaluator")

# Run these two agents after resume evaluation
builder.add_edge("resume_evaluator", "skill_gap")
builder.add_edge("resume_evaluator", "application_writer")

# Wait for both branches before quality review
builder.add_edge("skill_gap", "quality_reviewer")
builder.add_edge("application_writer", "quality_reviewer")

builder.add_edge("quality_reviewer", END)

# Build the graph
graph = builder.compile()
