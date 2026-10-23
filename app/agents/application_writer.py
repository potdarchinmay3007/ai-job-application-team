
from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_structured_llm
from app.models import ApplicationDraft
from app.state import JobApplicationState


SYSTEM_PROMPT = """
You are an Application Writer.

Write a professional job application using the candidate's resume
and the job requirements.

Rules:
- Use only facts supported by the resume.
- Never invent skills, experience, projects, or achievements.
- Do not claim missing skills as existing skills.
- Highlight relevant strengths honestly.
- Keep the cover letter concise and specific.
- Write a clear email subject and email body.
"""


def application_writer(state: JobApplicationState) -> dict:
    job = state["job_requirements"]
    evaluation = state["resume_evaluation"]

    message = f"""
    JOB REQUIREMENTS:
    {job.model_dump_json(indent=2)}

    RESUME:
    {state["resume_text"]}

    RESUME EVALUATION:
    {evaluation.model_dump_json(indent=2)}
    """

    llm = get_structured_llm(ApplicationDraft)

    result = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message),
        ]
    )

    return {"draft": result}
