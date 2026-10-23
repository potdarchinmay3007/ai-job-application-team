from langchain_core.messages import HumanMessage, SystemMessage

from app.llm import get_structured_llm
from app.models import ResumeEvaluation
from app.state import JobApplicationState

SYSTEM_PROMPT = """You are a resume evaluator.
You get a list of job requirements and a candidate's resume.

For every required and preferred skill:
- status "match" if the resume clearly shows it
- status "partial" if the resume shows something related but weaker
- status "missing" if the resume does not show it

Rules:
- The evidence must be text taken from the resume. Quote or closely copy it.
- If there is no evidence, write "none" and use status "missing".
- Never invent experience, skills, projects, or numbers.
- Do not guess. Only use what is written in the resume.

Also list the candidate's real strengths and give a match_score from 0 to 100."""


def resume_evaluator(state: JobApplicationState) -> dict:
    job = state["job_requirements"]
    message = (
        "JOB REQUIREMENTS:\n"
        f"{job.model_dump_json(indent=2)}\n\n"
        "RESUME:\n"
        f"{state['resume_text']}"
    )

    llm = get_structured_llm(ResumeEvaluation)
    result = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message),
        ]
    )
    return {"resume_evaluation": result}