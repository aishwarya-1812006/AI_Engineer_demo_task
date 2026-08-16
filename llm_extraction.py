import json
import time


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

MAX_CHUNK_SIZE = 4000

MAX_RETRIES = 5

BASE_WAIT_SECONDS = 2


# --------------------------------------------------
# Split large text into smaller chunks
# --------------------------------------------------

def chunk_text(text, max_size=MAX_CHUNK_SIZE):

    if not text:
        return []

    chunks = []

    for start in range(0, len(text), max_size):
        chunks.append(
            text[start:start + max_size]
        )

    return chunks


# --------------------------------------------------
# Exponential backoff
# --------------------------------------------------

def wait_before_retry(attempt):

    wait_time = BASE_WAIT_SECONDS * (2 ** attempt)

    print(
        f"Waiting {wait_time} seconds before retry..."
    )

    time.sleep(wait_time)


# --------------------------------------------------
# Convert extracted information into JSON
# --------------------------------------------------

def create_structured_record(
    entity_name,
    entity_type,
    source_url,
    extracted_data
):

    return {
        "schemaVersion": "1.0",

        "recordType": entity_type,

        "source": {
            "name": "LLM Extraction Pipeline",
            "url": source_url
        },

        "content": {
            "entityName": entity_name,
            "data": extracted_data
        }
    }


# --------------------------------------------------
# Simulated LLM extraction
#
# This function represents the provider call.
# A real provider can be connected here later.
# --------------------------------------------------

def extract_with_llm(text):

    chunks = chunk_text(text)

    print(
        f"Input contains {len(text)} characters."
    )

    print(
        f"Split into {len(chunks)} chunk(s)."
    )

    extracted_chunks = []

    for number, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"Processing chunk {number}/"
            f"{len(chunks)}..."
        )

        # Demonstration of structured extraction.
        #
        # In production, this section is replaced
        # by the actual LLM API request.

        extracted_chunks.append({
            "chunkNumber": number,
            "textLength": len(chunk),
            "extracted": True
        })

    return extracted_chunks


# --------------------------------------------------
# Handle provider responses
# --------------------------------------------------

def handle_provider_error(
    status_code,
    attempt
):

    # 413 = payload too large
    if status_code == 413:

        print(
            "413 Payload Too Large detected."
        )

        print(
            "The input should be split into "
            "smaller chunks."
        )

        return "CHUNK_INPUT"


    # 429 = rate limit
    if status_code == 429:

        print(
            "429 Rate Limit detected."
        )

        if attempt < MAX_RETRIES:

            wait_before_retry(attempt)

            return "RETRY"

        return "STOP"


    return "STOP"


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def run_pipeline():

    print()
    print("=" * 50)
    print("LLM EXTRACTION PIPELINE")
    print("=" * 50)
    print()

    sample_text = """
    OpenAI develops artificial intelligence systems.
    The company works on large language models,
    machine learning and generative AI.
    """

    result = extract_with_llm(
        sample_text
    )

    record = create_structured_record(
        entity_name="OpenAI",
        entity_type="STARTUP",
        source_url="https://example.com",
        extracted_data=result
    )

    print()
    print("Structured JSON output:")
    print()

    print(
        json.dumps(
            record,
            indent=4
        )
    )

    print()
    print("Pipeline completed successfully.")


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":

    run_pipeline()