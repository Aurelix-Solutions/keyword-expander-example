import csv
import json
import os

from apify_client import ApifyClient

ACTOR_ID = "aurelix/google-autocomplete-scraper"
RUN_INPUT = {
    "keywords": [
        "coffee maker"
    ],
    "sources": [
        "google",
        "youtube"
    ],
    "countries": [
        "us"
    ],
    "languages": [
        "en"
    ]
}
PREVIEW_FIELDS = ["keyword", "seed", "source", "country"]


def cell(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def main():
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR_ID).call(run_input=RUN_INPUT)
    dataset_id = run["defaultDatasetId"]
    items = list(client.dataset(dataset_id).iterate_items())

    for item in items[:5]:
        print(" | ".join(str(item.get(f, ""))[:80] for f in PREVIEW_FIELDS))
    print(f"{len(items)} results, dataset {dataset_id}")

    columns = []
    for item in items:
        for key in item:
            if key not in columns:
                columns.append(key)

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for item in items:
            writer.writerow({k: cell(item.get(k)) for k in columns})
    print("Wrote results.csv")


if __name__ == "__main__":
    main()
