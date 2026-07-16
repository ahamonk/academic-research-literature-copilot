from app.config import settings

_client = None


def _get_client():
    """
    Lazily create the Groq client on first use.
    """
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your .env file to use "
                "the Summarizer Agent."
            )
        from groq import Groq
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def summarize_paper(paper: dict) -> str:
    """
    Summarizer Agent: generate a single, concise summary of ONE paper,
    using only its title and abstract.

    Does NOT compare papers, identify trends, or combine multiple papers
    into a single review — combining per-paper summaries into a cohesive
    literature review is now the responsibility of the future Trend
    Analyzer agent, and validating each summary against its source
    abstract is the future Critic agent's responsibility.
    """
    prompt = (
        "Summarize the following research paper in 2-4 concise sentences, "
        "using ONLY the title and abstract provided below. Do not add "
        "information, citations, or claims that are not present in this "
        "text.\n\n"
        f"Title: {paper['title']}\n"
        f"Abstract: {paper['abstract']}"
    )

    client = _get_client()
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content