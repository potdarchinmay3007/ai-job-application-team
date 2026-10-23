
from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_structured_llm
from app.models import ReviewResult
from app.state import JobApplicationState


SYSTEM_PROMPT = """
You are a Quality Reviewer for job applications.

Check the cover letter and email against the candidate's resume.

Rules:
- Identify claims that are not supported by the resume.
- Never assume a skill or experience is real without evidence.
- Check whether the application is relevant to the job.
- Approve only if there are no unsupported claims.
- If unsupported claims exist, reject the draft and explain why.
- Return specific, useful feedback.
"""


def quality_reviewer(state: JobApplicationState) -> dict:
    draft = state["draft"]

    message = f"""
    CANDIDATE RESUME:
    {state["resume_text"]}

    JOB REQUIREMENTS:
    {state["job_requirements"].model_dump_json(indent=2)}

    APPLICATION DRAFT:
    {draft.model_dump_json(indent=2)}
    """

    llm = get_structured_llm(ReviewResult)

    result = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message),
        ]
    )

    return {"review": result}
