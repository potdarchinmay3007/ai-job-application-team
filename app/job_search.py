
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from app.resume_matcher import rank_jobs

SOURCES = {
    "Himalayas": "https://himalayas.app/jobs/api/search",
    "Remote OK": "https://remoteok.com/api",
    "Jobicy": "https://jobicy.com/api/v2/remote-jobs",
    "Remotive": "https://remotive.com/api/remote-jobs",
}

AI_KEYWORDS = (
    "artificial intelligence",
    "machine learning",
    "generative ai",
    "llm",
    "large language model",
    "python",
    "ai engineer",
    "deep learning",
    "data science",
)


def fetch_json(url: str) -> dict | list:
    """Download JSON from a public job API."""

    request = Request(
        url,
        headers={"User-Agent": "AI-Job-Application-Team/1.0"},
    )

    with urlopen(request, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def is_relevant(job: dict) -> bool:
    """Check whether a job is related to AI, ML, or Python."""

    text = (
        f"{job.get('title', '')} "
        f"{job.get('description', '')}"
    ).lower()

    return any(keyword in text for keyword in AI_KEYWORDS)



def is_allowed_job_type(job: dict) -> bool:
    """Keep internships and full-time jobs."""

    title = str(job.get("title") or "").lower()

    raw_job_type = job.get("job_type") or ""

    # Some APIs return a list; others return a string.
    if isinstance(raw_job_type, list):
        job_type = " ".join(
            str(item) for item in raw_job_type
        ).lower()
    else:
        job_type = str(raw_job_type).lower()

    job_type = job_type.replace("-", "_").replace(" ", "_")

    if "intern" in title or "intern" in job_type:
        return True

    return job_type in {
        "full_time",
        "fulltime",
    }



def is_worldwide(job: dict) -> bool:
    """Keep listings that explicitly indicate worldwide eligibility."""

    location = job.get("location", "").lower()

    worldwide_terms = (
        "worldwide",
        "anywhere",
        "global",
        "all countries",
        "open to all countries",
    )

    return any(term in location for term in worldwide_terms)


def normalize_job(
    title: str,
    company: str,
    job_type: str,
    location: str,
    description: str,
    url: str,
    source: str,
) -> dict:
    """Convert listings from different websites to one format."""

    return {
        "title": title or "Untitled role",
        "company": company or "Unknown",
        "job_type": job_type or "Not specified",
        "location": location or "Not specified",
        "description": description or "",
        "url": url or "",
        "source": source,
    }


def fetch_himalayas() -> list[dict]:
    """Fetch worldwide internships and full-time roles."""

    query = urlencode({
        "worldwide": "true",
        "employment_type": "Full Time,Intern",
        "page": 1,
    })

    data = fetch_json(f"{SOURCES['Himalayas']}?{query}")
    jobs = data.get("jobs", [])
    results = []

    for job in jobs:
        results.append(normalize_job(
            title=job.get("title", ""),
            company=job.get("companyName", ""),
            job_type=job.get("employmentType", ""),
            location="Worldwide",
            description=job.get("description") or job.get("excerpt", ""),
            url=job.get("applicationLink", ""),
            source="Himalayas",
        ))

    return results


def fetch_remote_ok() -> list[dict]:
    """Fetch listings from Remote OK."""

    data = fetch_json(SOURCES["Remote OK"])
    results = []

    if not isinstance(data, list):
        return results

    for job in data:
        # The first item may contain API legal information, not a job.
        if not isinstance(job, dict) or not job.get("position"):
            continue

        results.append(normalize_job(
            title=job.get("position", ""),
            company=job.get("company", ""),
            job_type=job.get("job_type", ""),
            location=job.get("location", ""),
            description=job.get("description", ""),
            url=job.get("url", ""),
            source="Remote OK",
        ))

    return results


def fetch_jobicy() -> list[dict]:
    """Fetch listings from Jobicy."""

    data = fetch_json(SOURCES["Jobicy"])
    results = []

    for job in data.get("jobs", []):
        results.append(normalize_job(
            title=job.get("jobTitle", ""),
            company=job.get("companyName", ""),
            job_type=job.get("jobType", ""),
            location=job.get("jobGeo", ""),
            description=job.get("jobDescription", ""),
            url=job.get("url", ""),
            source="Jobicy",
        ))

    return results


def fetch_remotive() -> list[dict]:
    """Fetch listings from Remotive."""

    data = fetch_json(SOURCES["Remotive"])
    results = []

    for job in data.get("jobs", []):
        results.append(normalize_job(
            title=job.get("title", ""),
            company=job.get("company_name", ""),
            job_type=job.get("job_type", ""),
            location=job.get("candidate_required_location", ""),
            description=job.get("description", ""),
            url=job.get("url", ""),
            source="Remotive",
        ))

    return results



def fetch_remote_jobs() -> list[dict]:
    """Fetch job listings from all sources and remove duplicates."""

    fetchers = [
        ("Himalayas", fetch_himalayas),
        ("Remote OK", fetch_remote_ok),
        ("Jobicy", fetch_jobicy),
        ("Remotive", fetch_remotive),
    ]

    all_jobs = []
    seen_jobs = set()

    for source_name, fetcher in fetchers:
        try:
            source_jobs = fetcher()
            print(f"{source_name}: retrieved {len(source_jobs)} listings.")

        except Exception as error:
            print(f"{source_name}: could not fetch listings ({error}).")
            continue

        for job in source_jobs:
            if not is_allowed_job_type(job):
                continue

            # Exclude duplicate listings across sources.
            unique_key = (
                job.get("url", "").lower().strip()
                or (
                    job.get("title", "").lower().strip(),
                    job.get("company", "").lower().strip(),
                )
            )

            if unique_key in seen_jobs:
                continue

            seen_jobs.add(unique_key)
            all_jobs.append(job)

    return all_jobs


def find_matching_jobs(resume_text: str) -> list[dict]:
    jobs = fetch_remote_jobs()
    return rank_jobs(resume_text, jobs)




if __name__ == "__main__":
    with open("data/sample_resume.md", "r", encoding="utf-8") as file:
        resume = file.read()

    jobs = find_matching_jobs(resume)

    print(f"\nRetrieved and evaluated {len(jobs)} listings.\n")

    for number, job in enumerate(jobs[:10], start=1):
        print(f"{number}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Match score: {job['match_score']}%")
        print(
            f"   Matched skills: "
            f"{', '.join(job['matched_skills']) or 'None detected'}"
        )
        print(
            f"   Missing skills: "
            f"{', '.join(job['missing_skills']) or 'None detected'}"
        )
        print(f"   Source: {job['source']}")
        print(f"   Apply: {job['url']}\n")


