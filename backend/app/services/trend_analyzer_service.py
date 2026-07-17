from app.config import settings

_client = None


def _get_client():
    """
    Lazily create the Groq client on first use — same pattern used in
    summarizer_service.py and critic_service.py.
    """
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your .env file to use "
                "the Trend Analyst Agent."
            )
        from groq import Groq
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def assign_citations(papers: list[dict]) -> list[dict]:
    """
    Assigns a 1-based citation number to each paper, in their existing
    order. Order is preserved unchanged from the Fetcher's semantic
    ranking through the Summarizer and Critic stages, so citation [1] is
    always the most relevant paper for the user's research interests.
    Assigned once here, before the Trend Analyst runs, so the same
    numbering is used consistently in both the generated review text and
    the references list.
    """
    return [{**paper, "citation": index} for index, paper in enumerate(papers, start=1)]


def generate_literature_review(cited_papers: list[dict]) -> str:
    """
    Trend Analyst Agent: reads ALL Critic-reviewed paper summaries
    together and generates ONE coherent literature review identifying
    common themes, emerging trends, common methodologies, and likely
    future research directions. A single Groq call for the entire
    review — no multi-pass reasoning, consistent with the simplicity of
    the Summarizer and Critic.

    `cited_papers` must already have a 'citation' number on each paper
    (see assign_citations) so the model can reference papers by number,
    matching the references list built from the same papers.
    """
    if not cited_papers:
        return "No papers were available to generate a literature review."

    papers_text = "\n\n".join(
        f"[{p['citation']}] Title: {p['title']}\nSummary: {p['summary']}"
        for p in cited_papers
    )

    prompt = (
        "You are a research assistant writing a weekly literature review "
        "based on the paper summaries below. Each paper is labeled with a "
        "citation number in brackets, e.g. [1].\n\n"
        f"{papers_text}\n\n"
        "Write a coherent literature review (3-6 paragraphs) that:\n"
        "- Identifies common research themes across these papers\n"
        "- Identifies emerging trends\n"
        "- Identifies common methodologies\n"
        "- Notes likely future research directions\n\n"
        "When referencing a paper, cite it using its bracketed number, "
        "e.g. \"Recent work increasingly focuses on retrieval-augmented "
        "generation [1][3].\" Only cite the papers listed above — do not "
        "invent citations, authors, or findings not present in the "
        "summaries."
    )

    client = _get_client()
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content


def build_references(cited_papers: list[dict]) -> list[dict]:
    """
    Builds the references list matching each paper's assigned citation
    number to its title and arXiv URL, for display alongside the
    generated literature review.
    """
    return [
        {"citation": p["citation"], "title": p["title"], "arxiv_url": p["arxiv_url"]}
        for p in cited_papers
    ]