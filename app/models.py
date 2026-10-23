from typing import Literal

from pydantic import BaseModel, Field


class JobRequirements(BaseModel):
    job_title: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    experience_requirements: list[str]


class SkillMatch(BaseModel):
    skill: str
    status: Literal["match", "partial", "missing"]
    evidence: str


class ResumeEvaluation(BaseModel):
    matches: list[SkillMatch]
    strengths: list[str]
    match_score: int = Field(ge=0, le=100)

class SkillGap(BaseModel):
    skill: str
    priority: Literal["high", "medium", "low"]
    learning_task: str
    portfolio_project: str


class SkillGapReport(BaseModel):
    gaps: list[SkillGap]


class ApplicationDraft(BaseModel):
    cover_letter: str
    email_subject: str
    email_body: str


class ReviewResult(BaseModel):
    approved: bool
    unsupported_claims: list[str]
    feedback: str