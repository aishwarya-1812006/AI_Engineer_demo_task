import requests
import csv

url = "https://raw.githubusercontent.com/yc-oss/api/main/companies/top.json"

response = requests.get(url)
data = response.json()

companies = data[:5]

with open("startup_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Name",
        "Website",
        "Location",
        "Industry",
        "Team Size",
        "Batch",
        "Status"
    ])

    for company in companies:
        writer.writerow([
            company.get("name"),
            company.get("website"),
            company.get("all_locations"),
            company.get("industry"),
            company.get("team_size"),
            company.get("batch"),
            company.get("status")
        ])

print("Successfully saved 5 startup records to startup_data.csv")