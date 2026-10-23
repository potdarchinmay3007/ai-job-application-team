
from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_structured_llm
from app.models import SkillGapReport
from app.state import JobApplicationState


SYSTEM_PROMPT = """
You are a Skill Gap Agent.

Read the job requirements and resume evaluation.

1. Find skills marked "missing" or "partial".
2. Give each skill a priority: high, medium, or low.
3. Suggest a practical learning task for each skill.
4. Suggest a small portfolio project for each skill.
5. Do not invent skills or candidate experience.
6. Ignore skills marked "match".
7. If there are no skill gaps, return an empty gaps list.
"""


def skill_gap_agent(state: JobApplicationState) -> dict:
    job = state["job_requirements"]
    evaluation = state["resume_evaluation"]

    message = f"""
    JOB REQUIREMENTS:
    {job.model_dump_json(indent=2)}

    RESUME EVALUATION:
    {evaluation.model_dump_json(indent=2)}
    """

    llm = get_structured_llm(SkillGapReport)

    result = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message),
        ]
    )

    return {"skill_gap_report": result}
