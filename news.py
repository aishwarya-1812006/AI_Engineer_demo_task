import requests
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from urllib.parse import quote


# -----------------------------------------
# SETTINGS
# -----------------------------------------

BASE_URL = "https://news.google.com/rss/search"

QUERIES = [
    "artificial intelligence",
    "AI technology",
    "machine learning",
    "generative AI",
    "AI startup",
    "AI research",
    "deep learning",
    "computer vision",
    "natural language processing"
]

# Only keep news from the last 24 hours
cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)

articles = []
seen_urls = set()


# -----------------------------------------
# GET NEWS
# -----------------------------------------

print("Getting fresh AI news from Google News...")
print("Only articles from the last 24 hours will be saved.")
print()


for query in QUERIES:

    print(f"Searching for: {query}")

    search_query = f"{query} when:1d"

    url = (
        BASE_URL
        + "?q="
        + quote(search_query)
        + "&hl=en-IN"
        + "&gl=IN"
        + "&ceid=IN:en"
    )

    try:

        response = requests.get(
            url,
            timeout=60,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        print("Status code:", response.status_code)

        response.raise_for_status()

    except requests.exceptions.RequestException as error:

        print("Request failed:")
        print(error)
        continue


    # -----------------------------------------
    # READ RSS XML
    # -----------------------------------------

    try:

        root = ET.fromstring(response.content)

    except ET.ParseError as error:

        print("Could not read RSS feed:")
        print(error)
        continue


    # -----------------------------------------
    # PROCESS ARTICLES
    # -----------------------------------------

    for item in root.findall(".//item"):

        title_element = item.find("title")
        link_element = item.find("link")
        date_element = item.find("pubDate")
        source_element = item.find("source")
        description_element = item.find("description")


        if (
            title_element is None
            or link_element is None
            or date_element is None
        ):
            continue


        title = (
            title_element.text or ""
        ).strip()

        article_url = (
            link_element.text or ""
        ).strip()

        published_text = (
            date_element.text or ""
        ).strip()


        source_name = ""

        if source_element is not None:
            source_name = (
                source_element.text or ""
            ).strip()


        description = ""

        if description_element is not None:
            description = (
                description_element.text or ""
            ).strip()


        # -----------------------------------------
        # PARSE PUBLICATION DATE
        # -----------------------------------------

        try:

            published_time = datetime.strptime(
                published_text,
                "%a, %d %b %Y %H:%M:%S %Z"
            ).replace(
                tzinfo=timezone.utc
            )

        except ValueError:

            try:

                published_time = datetime.strptime(
                    published_text,
                    "%a, %d %b %Y %H:%M:%S %z"
                )

            except ValueError:

                continue


        # -----------------------------------------
        # LAST 24 HOURS CHECK
        # -----------------------------------------

        if published_time < cutoff_time:
            continue


        # -----------------------------------------
        # REMOVE DUPLICATES
        # -----------------------------------------

        if article_url in seen_urls:
            continue

        seen_urls.add(article_url)


        # -----------------------------------------
        # SAVE ARTICLE
        # -----------------------------------------

        articles.append({

            "schemaVersion": "1.0",

            "recordType": "NEWS",

            "source.name":
                source_name,

            "source.url":
                article_url,

            "content.title":
                title,

            "content.description":
                description,

            "content.publishedAt":
                published_time.isoformat(),

            "content.topic":
                query,

            "collectedAt":
                datetime.now(
                    timezone.utc
                ).isoformat()
        })


    print(
        "Fresh articles collected so far:",
        len(articles)
    )

    print()


# -----------------------------------------
# SORT BY NEWEST FIRST
# -----------------------------------------

articles.sort(
    key=lambda x:
    x["content.publishedAt"],
    reverse=True
)


# -----------------------------------------
# SAVE CSV
# -----------------------------------------

with open(
    "news.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [

        "schemaVersion",

        "recordType",

        "source.name",

        "source.url",

        "content.title",

        "content.description",

        "content.publishedAt",

        "content.topic",

        "collectedAt"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(articles)


# -----------------------------------------
# FINAL RESULT
# -----------------------------------------

print()
print(
    "-----------------------------------------"
)

print(
    f"Successfully saved "
    f"{len(articles)} fresh AI news articles "
    f"to news.csv"
)

print(
    "Only articles published within "
    "the last 24 hours were included."
)

print(
    "-----------------------------------------"
)