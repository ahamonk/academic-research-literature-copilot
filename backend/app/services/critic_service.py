from app.config import settings

_client = None


def _get_client():
    """
    Lazily create the Groq client on first use — same pattern used in
    summarizer_service.py. Reuses the same GROQ_API_KEY/GROQ_MODEL config;
    no new client, no new settings needed.
    """
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your .env file to use "
                "the Critic Agent."
            )
        from groq import Groq
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def review_summary(paper: dict) -> str:
    """
    Critic Agent: compares a single paper's generated summary against its
    original abstract, and returns a reviewed (corrected/improved) summary.

    `paper` must contain at least 'abstract' and 'summary' (the abstract
    from PostgreSQL, and the draft summary produced by the Summarizer
    Agent for this same paper).

    One single Groq call, no multi-step reasoning — consistent with the
    Summarizer's own "keep it simple" design. The Critic does not compare
    across papers and does not generate a literature review; it only
    reviews one paper's own summary against its own abstract.
    """
    prompt = (
        "You are reviewing an AI-generated summary of a research paper "
        "abstract for accuracy and clarity.\n\n"
        f"Original Abstract:\n{paper['abstract']}\n\n"
        f"Generated Summary:\n{paper['summary']}\n\n"
        "Compare the summary against the abstract. If the summary contains "
        "any inaccuracy, missing important technical detail, or unclear "
        "phrasing, rewrite it to fix those issues while staying concise "
        "(2-4 sentences). If the summary is already accurate and clear, "
        "return it unchanged. Do not add any information that is not "
        "present in the original abstract. Respond with ONLY the final "
        "summary text, no preamble or explanation."
    )

    client = _get_client()
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()