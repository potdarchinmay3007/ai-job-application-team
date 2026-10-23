from langchain_core.messages import HumanMessage, SystemMessage

from app.llm import get_structured_llm
from app.models import JobRequirements
from app.state import JobApplicationState

SYSTEM_PROMPT = """You are a job analyst.
Read the job description and extract:
- the job title
- required skills
- preferred (nice-to-have) skills
- main responsibilities
- experience or education requirements

Use only what the job description says. Do not add skills that are not mentioned.
If something is not mentioned, return an empty list."""


def job_analyst(state: JobApplicationState) -> dict:
    llm = get_structured_llm(JobRequirements)
    result = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["job_description"]),
        ]
    )
    return {"job_requirements": result}