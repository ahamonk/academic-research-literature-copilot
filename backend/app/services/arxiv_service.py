import feedparser
import requests

ARXIV_API_URL = "http://export.arxiv.org/api/query"


def fetch_papers_from_arxiv(category: str, max_results: int = 20) -> list[dict]:
    """
    Fetch recent papers from the arXiv API for a given category code (e.g. 'cs.AI').
    Returns a list of dicts with keys matching the Paper model's fields.
    """
    params = {
        "search_query": f"cat:{category}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }

    response = requests.get(ARXIV_API_URL, params=params, timeout=30)
    response.raise_for_status()

    feed = feedparser.parse(response.text)

    papers = []
    for entry in feed.entries:
        papers.append(_parse_entry(entry, category))

    return papers


def _parse_entry(entry, requested_category: str) -> dict:
    # arXiv IDs come back as a full URL, e.g. http://arxiv.org/abs/2401.12345v2
    arxiv_id = entry.id.split("/abs/")[-1]

    authors = ", ".join(author.name for author in entry.authors)

    primary_category = entry.get("arxiv_primary_category", {}).get(
        "term", requested_category
    )

    published_date = entry.published[:10]  # "2024-01-15T00:00:00Z" -> "2024-01-15"

    return {
        "arxiv_id": arxiv_id,
        "title": entry.title.strip().replace("\n", " "),
        "abstract": entry.summary.strip().replace("\n", " "),
        "authors": authors,
        "published_date": published_date,
        "arxiv_url": entry.id,
        "primary_category": primary_category,
    }