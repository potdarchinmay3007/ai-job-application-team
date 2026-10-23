from app.graph import graph

def main():
    # Read the sample resume
    with open("data/sample_resume.md", "r", encoding="utf-8") as file:
        resume = file.read()

    # Read the sample job description
    with open("data/sample_job.txt", "r", encoding="utf-8") as file:
        job_description = file.read()

    print("Running AI Job Application Team...")

    # Run all five agents
    result = graph.invoke({
        "resume_text": resume,
        "job_description": job_description,
        "revision_count": 0,
    })

    # Display the results
    print("\n===== JOB REQUIREMENTS =====")
    print(result["job_requirements"].model_dump_json(indent=2))

    print("\n===== RESUME EVALUATION =====")
    print(result["resume_evaluation"].model_dump_json(indent=2))

    print("\n===== SKILL GAPS =====")
    print(result["skill_gap_report"].model_dump_json(indent=2))

    print("\n===== APPLICATION DRAFT =====")
    print(result["draft"].model_dump_json(indent=2))

    print("\n===== QUALITY REVIEW =====")
    print(result["review"].model_dump_json(indent=2))


if __name__ == "__main__":
    main()
