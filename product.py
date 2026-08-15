import requests
import csv
from datetime import datetime, timezone

# Verified public AI tools dataset
url = "https://raw.githubusercontent.com/LichAmnesia/awesome-ai-tools-dataset/main/data.csv"

response = requests.get(url, timeout=30)
response.raise_for_status()

reader = csv.DictReader(response.text.splitlines())

products = []
seen_names = set()

for row in reader:
    name = row.get("Title", "").strip()
    website = row.get("Website", "").strip()

    if not name or name in seen_names:
        continue

    seen_names.add(name)

    products.append({
        "schemaVersion": "1.0",
        "recordType": "PRODUCT",
        "source.name": "Awesome AI Tools Dataset",
        "source.url": url,
        "content.startupName": "",
        "content.productName": name,
        "content.pricingModel": "UNKNOWN",
        "content.website": website,
        "collectedAt": datetime.now(timezone.utc).isoformat()
    })

    if len(products) >= 1000:
        break

# Save product data
with open("product_data.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "schemaVersion",
        "recordType",
        "source.name",
        "source.url",
        "content.startupName",
        "content.productName",
        "content.pricingModel",
        "content.website",
        "collectedAt"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

print(f"Successfully saved {len(products)} product records to product_data.csv")