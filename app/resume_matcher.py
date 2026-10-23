
import re


SKILL_KEYWORDS = {
    "python": ["python"],
    "machine learning": ["machine learning"],
    "deep learning": ["deep learning"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "llm": ["llm", "large language model", "large language models"],
    "generative ai": ["generative ai", "genai"],
    "rag": ["rag", "retrieval augmented generation"],
    "langchain": ["langchain"],
    "langgraph": ["langgraph"],
    "hugging face": ["hugging face", "transformers"],
    "api": ["api", "apis", "rest api", "rest apis"],
    "git": ["git", "github"],
    "sql": ["sql"],
    "data science": ["data science"],
    "neural networks": ["neural network", "neural networks"],
    "agents": ["ai agent", "ai agents", "agentic ai", "multi-agent"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "java": ["java"],
    "javascript": ["javascript"],
    "typescript": ["typescript"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes"],
}


AI_ROLE_TERMS = [
    "artificial intelligence", "machine learning",
    "deep learning", "llm", "generative ai",
    "ai engineer", "ai developer", "ai agent",
    "rag", "nlp", "computer vision",
]

SOFTWARE_ROLE_TERMS = [
    "software engineer", "software developer",
    "backend developer", "back-end developer",
    "back end developer", "frontend developer",
    "front-end developer", "full stack developer",
    "full-stack developer", "python developer",
    "web developer", "application developer",
    "systems engineer",
]

ENTRY_LEVEL_TERMS = [
    "intern", "internship", "junior", "entry level",
    "entry-level", "graduate", "new grad", "trainee",
]

SENIOR_TITLE_TERMS = [
    "senior", "staff", "principal", "tech lead",
    "technical lead", "team lead", "director",
    "head of", "chief ", "manager",
]

EXPERIENCE_REQUIREMENTS = [
    "7+ years", "8+ years", "10+ years",
    "7 years of experience", "8 years of experience",
    "10 years of experience",
]


def find_skills(text: str) -> set[str]:
    """Find known skills using word-boundary-aware matching."""
    text = text.lower()
    found_skills = set()

    for skill, variations in SKILL_KEYWORDS.items():
        for variation in variations:
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(variation)
                + r"(?![a-z0-9])"
            )
            if re.search(pattern, text):
                found_skills.add(skill)
                break

    return found_skills


def match_job_to_resume(resume_text: str, job: dict) -> dict:
    """Estimate skill coverage and flag possible seniority mismatch."""

    title = job.get("title", "")
    description = job.get("description", "")
    title_lower = title.lower()
    description_lower = description.lower()
    job_text = f"{title} {description}"

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_text)

    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    # Score is based on the proportion of detected job skills
    # found in the resume. No automatic role or intern bonus.
    if job_skills:
        skill_score = round(
            100 * len(matched_skills) / len(job_skills)
        )
    else:
        skill_score = 0

    is_ai_role = any(
        term in job_text.lower() for term in AI_ROLE_TERMS
    )
    is_software_role = any(
        term in title_lower for term in SOFTWARE_ROLE_TERMS
    )
    is_entry_level = any(
        term in title_lower for term in ENTRY_LEVEL_TERMS
    )
    is_senior = (
        any(term in title_lower for term in SENIOR_TITLE_TERMS)
        or any(
            term in description_lower
            for term in EXPERIENCE_REQUIREMENTS
        )
    )

    # A role-fit warning is reported separately from skill coverage.
    # This avoids silently changing the skill score with arbitrary bonuses.
    return {
        **job,
        "match_score": skill_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "is_ai_role": is_ai_role,
        "is_software_role": is_software_role,
        "is_entry_level": is_entry_level,
        "is_senior": is_senior,
        "role_warning": (
            "May require more experience than shown in the resume."
            if is_senior
            else ""
        ),
        "score_note": (
            "Percentage of detected job skills found in the resume; "
            "not a hiring probability or full requirement assessment."
        ),
    }


def rank_jobs(resume_text: str, jobs: list[dict]) -> list[dict]:
    """Rank jobs by detected skill coverage, highest first."""
    ranked_jobs = [
        match_job_to_resume(resume_text, job)
        for job in jobs
    ]

    return sorted(
        ranked_jobs,
        key=lambda job: job["match_score"],
        reverse=True,
    )
