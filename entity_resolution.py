import csv
import re
from collections import defaultdict


INPUT_FILE = "startup_data.csv"
OUTPUT_FILE = "entity_mapping_log.csv"


# --------------------------------------------------
# Normalize a company/entity name
# --------------------------------------------------

def normalize_name(name):

    if not name:
        return ""

    name = name.strip()

    # Convert to lowercase
    name = name.lower()

    # Remove common legal company suffixes
    name = re.sub(
        r"\b(incorporated|inc|corp|corporation|"
        r"company|co|ltd|limited|llc|plc)\b\.?",
        "",
        name
    )

    # Remove punctuation
    name = re.sub(r"[^a-z0-9\s]", "", name)

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name


# --------------------------------------------------
# Create a readable canonical name
# --------------------------------------------------

def canonical_name(original_name):

    normalized = normalize_name(original_name)

    if not normalized:
        return ""

    # Use the original spelling as the canonical
    # display name, after removing legal suffixes.
    words = normalized.split()

    return " ".join(
        word.capitalize()
        for word in words
    )


# --------------------------------------------------
# Read startup records
# --------------------------------------------------

records = []

with open(
    INPUT_FILE,
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        original_name = (
            row.get("content.entityName", "")
            or row.get("Name", "")
        ).strip()

        source_url = (
            row.get("source.url", "")
            or row.get("Website", "")
        ).strip()

        if not original_name:
            continue

        records.append({
            "original_name": original_name,
            "source_url": source_url
        })


# --------------------------------------------------
# Group entities using normalized names
# --------------------------------------------------

groups = defaultdict(list)

for record in records:

    normalized = normalize_name(
        record["original_name"]
    )

    if normalized:
        groups[normalized].append(record)


# --------------------------------------------------
# Create entity mapping log
# --------------------------------------------------

mapping_rows = []

for normalized, group in groups.items():

    # Choose the first real source name as canonical
    canonical = group[0]["original_name"]

    for record in group:

        original = record["original_name"]

        if original == canonical:
            resolution_method = "EXACT_MATCH"
        else:
            resolution_method = "NORMALIZED_MATCH"

        mapping_rows.append({

            "originalName": original,

            "canonicalName": canonical,

            "normalizedName": normalized,

            "resolutionMethod": resolution_method,

            "sourceUrl": record["source_url"]

        })


# --------------------------------------------------
# Save mapping log
# --------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
        "originalName",
        "canonicalName",
        "normalizedName",
        "resolutionMethod",
        "sourceUrl"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(mapping_rows)


# --------------------------------------------------
# Final result
# --------------------------------------------------

print()
print(
    f"Processed {len(records)} startup records."
)

print(
    f"Found {len(groups)} normalized entities."
)

print(
    f"Successfully saved entity mapping log to "
    f"{OUTPUT_FILE}"
)