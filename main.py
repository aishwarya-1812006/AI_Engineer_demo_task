from idlelib import statusbar

import requests
import csv
from datetime import datetime, timezone

# YC Companies API - all launched companies
url = "https://yc-oss.github.io/api/companies/all.json"

# Get the data
response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()

# Take the first 1000 companies
companies = data[:1000]

# Create startup CSV
with open("startup_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow([
        "schemaVersion",
        "recordType",
        "source.name",
        "source.url",
        "content.entityName",
        "content.data.employeeCount",
        "collectedAt"
    ])

    # Write company records
    for company in companies:
        writer.writerow([
            "1.0",
            "STARTUP",
            "Y Combinator",
            company.get("url", ""),
            company.get("name", ""),
            company.get("team_size", ""),
            datetime.now(timezone.utc).isoformat()
        ])

print(f"Successfully saved {len(companies)} startup records to startup_data.csv")