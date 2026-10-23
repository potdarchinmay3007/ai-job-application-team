from typing import TypedDict

from app.models import (
    ApplicationDraft,
    JobRequirements,
    ResumeEvaluation,
    ReviewResult,
    SkillGapReport,
)


class JobApplicationState(TypedDict, total=False):
    # What you give the app
    job_description: str
    resume_text: str

    # What each agent writes back
    job_requirements: JobRequirements
    resume_evaluation: ResumeEvaluation
    skill_gap_report: SkillGapReport
    draft: ApplicationDraft
    review: ReviewResult

    # Used to control the flow
    revision_count: int
    human_decision: str