# Google Autocomplete Scraper: Python example

**Google Autocomplete API - Autosuggest Keyword Ideas.** Expands seed keywords into hundreds of real Google and YouTube autocomplete phrases, tagged by search intent. Price, example input and output, and FAQ: [Google Autocomplete API on the Aurelix tools site](https://aurelix-solutions.github.io/tools/google-autocomplete-scraper/). Run it on the Apify Store: [apify.com/aurelix/google-autocomplete-scraper](https://apify.com/aurelix/google-autocomplete-scraper).


A small, runnable example for [Google Autocomplete Scraper](https://apify.com/aurelix/google-autocomplete-scraper), an Apify Actor by Aurelix.

## What it does

Google Autocomplete Scraper turns each seed keyword into hundreds of real search phrases from Google Search and YouTube autocomplete. It queries the seed on its own and with every modifier you pick (a to z, 0 to 9, question words such as how, what and why, and prepositions such as for, with, near and vs), for every country and language you list, then removes duplicates and tags each phrase's intent: question, commercial, local or comparison. Depth 2 re-queries each new suggestion for a long-tail tree.

## Why this over alternatives

Compared with the leading alternatives on the Apify Store (the same table is on the Store page):

| | **This Actor** | automation-lab/google-autocomplete-scraper | memo23/google-suggest-scraper |
|---|---|---|---|
| **Price per 1,000 keywords, free plan** | $0.45 | $1.00 | $0.50 |
| **Price per 1,000 keywords, paid plans** | $0.35 | $0.90 | $0.50 |
| **Start fee per run** | $0.0005 | $0.005 | $0.005 |
| **Platform usage billed on top** | No | No | No |
| **YouTube autocomplete** | ✓ | ✗ (Google only) | ✗ (Google only) |
| **A-Z modifiers** | ✓ | ✓ | ✓ |
| **Question and preposition modifiers** | 6 languages | English question words | English question words |
| **Several countries and languages in one run** | ✓ | ✗ (one each) | ✓ |
| **Intent tags (question, commercial, local, comparison)** | ✓ | not stated | not stated |

- Google and YouTube in one run, with a country and language grid.
- A-Z, 0-9, question and preposition modifiers in six languages.
- Duplicates removed per source and market; you pay only for unique keywords.
- Intent tags on every keyword: question, commercial, local, comparison.
- $0.45 per 1,000 keywords ($0.35 on paid plans) and a $0.0005 start fee.
- Polite pace with retries; a throttled run still ends with what it collected.

## When to use it

- SEO writers building topic clusters and FAQ sections from real question searches
- YouTube creators finding video titles people actually type
- PPC managers collecting commercial and local long-tail phrases per country
- AI agents that need keyword ideas for a brief through MCP

## Input example

This is the `google-youtube-keyword-ideas` input used in `main.py`:

```json
{
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
```

Every input field is documented on the [Store page](https://apify.com/aurelix/google-autocomplete-scraper).

## How to run

1. Get an Apify API token from Apify Console (Settings, API & Integrations).
2. Install and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APIFY_TOKEN=your_token_here
python main.py
```

The script starts a run of `aurelix/google-autocomplete-scraper`, prints a few fields from the first results and writes every result to `results.csv`. Lists and nested objects are stored in the CSV as JSON text. Each run is billed to your Apify account (see Pricing below).

## Sample output

One record as returned by a real run (long text is shortened):

```json
{
  "keyword": "how coffee maker works",
  "seed": "coffee maker",
  "source": "google",
  "country": "US",
  "language": "en",
  "modifier": "how",
  "query": "how coffee maker",
  "position": 1,
  "depth": 1,
  "intents": [
    "question"
  ],
  "word_count": 4,
  "source_url": "https://suggestqueries.google.com/complete/search?client=firefox&q=how+coffee+maker&hl=en&gl=us",
  "scraped_at": "2026-11-04T18:52:26Z"
}
```

## Export to CSV

`main.py` writes `results.csv` with the `csv` module. You can also download any run's results directly:

```
https://api.apify.com/v2/datasets/<datasetId>/items?format=csv&clean=true
```

Send your token in an `Authorization: Bearer <token>` header (or `?token=`) if the dataset is not readable without one. Other formats: `format=json`, `format=xlsx`.

## Google Sheets

- Simplest: use Apify's Google Sheets integration on the Actor or a saved task, so each run's results land in a sheet with no token in the sheet itself.
- Quick pull of one run: `=IMPORTDATA("https://api.apify.com/v2/datasets/<datasetId>/items?format=csv&clean=true")`. This only works without a token if your account lets anyone with the dataset ID read it. Do not paste an API token into a sheet formula: anyone who can view or copy the sheet can read it and use your account.

## n8n

- Apify node: choose "Run an Actor", enter `aurelix/google-autocomplete-scraper`, paste the input above, then read the run's dataset items.
- HTTP Request node: `POST https://api.apify.com/v2/acts/aurelix~google-autocomplete-scraper/run-sync-get-dataset-items` with header `Authorization: Bearer <token>` (stored as an n8n credential) and the input as the JSON body. The response is the list of results. This endpoint waits for the run to finish, so for large runs start the run asynchronously and fetch the dataset when it ends.

## Limits

- Phrases that contain a phone number or an email address are dropped and not charged.
- No search volume, CPC or difficulty: autocomplete gives phrases and their order only.
- The suggestion box this Actor reads returns at most 10 suggestions per query (Chrome's address bar can show up to 15 from a different Google client, which is not used), so the yield per seed is bounded by the number of modifiers (about 60 queries per seed, source and market at depth 1).
- Suggestions change over time and Google personalises them by location; the country setting localises them, but results from a datacenter IP can differ slightly from what a signed-in user sees.
- Intent tags come from word rules, not a model; rare phrasings can be missed or mis-tagged.
- At most 20 country x language combinations per run, and depth at most 2.
- Speed: about 1 to 3 requests a second through the proxy, roughly 400 to 1,000 keywords a minute; a seed with every modifier on two sources takes about a minute.
- Google can throttle datacenter IPs; the run then stops early with the keywords collected so far.

## Pricing

At the time of writing:

Pay per event: you pay only for what the run returns, plus a small start fee.

| Event | Free plan | Paid plans (Bronze, Silver, Gold) |
|---|---|---|
| `keyword-result` | $0.45 per 1,000 keywords | $0.35 per 1,000 keywords |
| `apify-actor-start` | $0.0005 per run | $0.0005 per run |

Only unique keywords are charged: a phrase that repeats in the same source, country and language is skipped for free. A seed with no suggestions of its own is not expanded, so nonsense input costs only the $0.0005 start fee.

Check the [Store page](https://apify.com/aurelix/google-autocomplete-scraper) for current prices.

## Links

- Actor: https://apify.com/aurelix/google-autocomplete-scraper
- Questions, bugs and feature requests: the Issues tab on the Store page.

## Licence

The example code in this repository is released under the MIT licence (see `LICENSE`). The Actor itself runs on Apify and is billed through your Apify account.
