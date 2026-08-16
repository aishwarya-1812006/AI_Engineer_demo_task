import requests
import csv
from datetime import datetime, timezone, timedelta


# -----------------------------------------
# SETTINGS
# -----------------------------------------

API_URL = "https://himalayas.app/jobs/api"

MAX_PAGES = 10
LIMIT = 20

# Jobs must have been published within the last 24 hours
cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)

jobs_found = []


# -----------------------------------------
# GET JOBS
# -----------------------------------------

print("Getting recent AI/ML jobs from Himalayas...")
print()

for page in range(MAX_PAGES):

    offset = page * LIMIT

    print(f"Requesting jobs {offset + 1} to {offset + LIMIT}...")

    params = {
        "limit": LIMIT,
        "offset": offset
    }

    try:

        response = requests.get(
            API_URL,
            params=params,
            timeout=60
        )

        print("Status code:", response.status_code)

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as error:

        print("Request failed:")
        print(error)
        break


    jobs = data.get("jobs", [])

    if not jobs:
        print("No more jobs available.")
        break


    # -----------------------------------------
    # FILTER AI / ML JOBS FROM LAST 24 HOURS
    # -----------------------------------------

    for job in jobs:

        title = job.get("title", "")
        description = job.get("description", "")
        categories = job.get("categories", [])
        pub_date = job.get("pubDate")

        search_text = (
            title + " " +
            description + " " +
            " ".join(categories)
        ).lower()


        # AI / ML keywords
        ai_keywords = [
            "artificial intelligence",
            "machine learning",
            "ai engineer",
            "ml engineer",
            "deep learning",
            "generative ai",
            "genai",
            "computer vision",
            "nlp",
            "natural language processing",
            "data scientist",
            "ai/ml"
        ]

        is_ai_job = any(
            keyword in search_text
            for keyword in ai_keywords
        )


        if not is_ai_job:
            continue


        # -----------------------------------------
        # CHECK 24-HOUR FRESHNESS
        # -----------------------------------------

        if not pub_date:
            continue

        try:

            published_time = datetime.fromtimestamp(
                pub_date / 1000,
                tz=timezone.utc
            )

        except (TypeError, ValueError, OSError):

            continue


        if published_time < cutoff_time:
            continue


        jobs_found.append({

            "schemaVersion": "1.0",

            "recordType": "JOB",

            "source.name": "Himalayas",

            "source.url": job.get(
                "applicationLink",
                ""
            ),

            "content.jobTitle": title,

            "content.companyName": job.get(
                "companyName",
                ""
            ),

            "content.employmentType": job.get(
                "employmentType",
                ""
            ),

            "content.seniority": ", ".join(
                job.get("seniority", [])
            ),

            "content.categories": ", ".join(
                categories
            ),

            "content.publishedAt":
                published_time.isoformat(),

            "content.applicationLink":
                job.get(
                    "applicationLink",
                    ""
                ),

            "collectedAt":
                datetime.now(
                    timezone.utc
                ).isoformat()
        })


    print(
        f"Fresh AI/ML jobs collected so far: "
        f"{len(jobs_found)}"
    )

    # Stop if we have enough
    if len(jobs_found) >= 100:
        break


# -----------------------------------------
# SAVE CSV
# -----------------------------------------

with open(
    "jobs.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [

        "schemaVersion",

        "recordType",

        "source.name",

        "source.url",

        "content.jobTitle",

        "content.companyName",

        "content.employmentType",

        "content.seniority",

        "content.categories",

        "content.publishedAt",

        "content.applicationLink",

        "collectedAt"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(jobs_found)


# -----------------------------------------
# FINAL RESULT
# -----------------------------------------

print()
print(
    f"Successfully saved "
    f"{len(jobs_found)} fresh AI/ML jobs "
    f"to jobs.csv"
)