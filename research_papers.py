import requests
import csv
import time
import xml.etree.ElementTree as ET


# -----------------------------
# SETTINGS
# -----------------------------

BASE_URL = "https://export.arxiv.org/api/query"

TOTAL_PAPERS = 1000
BATCH_SIZE = 50

papers = []


# -----------------------------
# START
# -----------------------------

print("Getting 1000 AI research papers from arXiv...")
print("Please wait...")
print()


# -----------------------------
# GET PAPERS IN SMALL BATCHES
# -----------------------------

for start in range(0, TOTAL_PAPERS, BATCH_SIZE):

    end = min(start + BATCH_SIZE, TOTAL_PAPERS)

    print(f"Getting papers {start + 1} to {end}...")

    params = {
        "search_query": "cat:cs.AI",
        "start": start,
        "max_results": BATCH_SIZE,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    success = False

    # Try each batch up to 3 times
    for attempt in range(1, 4):

        try:

            response = requests.get(
                BASE_URL,
                params=params,
                timeout=(30, 120)
            )

            print("Status code:", response.status_code)

            # Too many requests
            if response.status_code == 429:

                print("Too many requests.")
                print("Waiting 15 seconds before trying again...")

                time.sleep(15)
                continue

            response.raise_for_status()

            # Read XML response
            root = ET.fromstring(response.text)

            namespace = {
                "atom": "http://www.w3.org/2005/Atom"
            }

            batch_count = 0

            # -----------------------------
            # READ EACH PAPER
            # -----------------------------

            for entry in root.findall("atom:entry", namespace):

                title = entry.find(
                    "atom:title",
                    namespace
                )

                summary = entry.find(
                    "atom:summary",
                    namespace
                )

                published = entry.find(
                    "atom:published",
                    namespace
                )

                paper_id = entry.find(
                    "atom:id",
                    namespace
                )

                authors = []

                for author in entry.findall(
                    "atom:author",
                    namespace
                ):

                    name = author.find(
                        "atom:name",
                        namespace
                    )

                    if name is not None:
                        authors.append(
                            name.text.strip()
                        )

                paper = {
                    "Title":
                        title.text.strip()
                        if title is not None
                        else "",

                    "Authors":
                        ", ".join(authors),

                    "Abstract":
                        summary.text.strip()
                        if summary is not None
                        else "",

                    "Published":
                        published.text.strip()
                        if published is not None
                        else "",

                    "URL":
                        paper_id.text.strip()
                        if paper_id is not None
                        else ""
                }

                papers.append(paper)

                batch_count += 1

            print(
                f"Collected {batch_count} papers "
                f"(Total: {len(papers)})"
            )

            success = True

            # Wait before the next batch
            time.sleep(5)

            break

        except requests.exceptions.Timeout:

            print(
                f"Timeout on attempt {attempt}/3."
            )

            if attempt < 3:
                print("Waiting 10 seconds...")
                time.sleep(10)

        except requests.exceptions.RequestException as error:

            print(
                f"Request error on attempt "
                f"{attempt}/3:"
            )

            print(error)

            if attempt < 3:
                print("Waiting 10 seconds...")
                time.sleep(10)

        except ET.ParseError:

            print(
                f"Could not read arXiv response "
                f"on attempt {attempt}/3."
            )

            if attempt < 3:
                print("Waiting 10 seconds...")
                time.sleep(10)

    # If all 3 attempts failed
    if not success:

        print(
            f"Could not collect papers "
            f"{start + 1} to {end}."
        )

        print(
            "Stopping collection safely."
        )

        break


# -----------------------------
# SAVE TO CSV
# -----------------------------

print()
print("Saving collected papers...")


with open(
    "research_papers.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
        "Title",
        "Authors",
        "Abstract",
        "Published",
        "URL"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(papers)


# -----------------------------
# FINAL MESSAGE
# -----------------------------

print()

print(
    f"Successfully saved "
    f"{len(papers)} research papers "
    f"to research_papers.csv"
)

print()

print("Research paper collection completed!")