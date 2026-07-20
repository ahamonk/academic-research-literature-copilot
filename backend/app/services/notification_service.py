from sqlalchemy.orm import Session

from app.models.user import User
from app.services.review_service import generate_weekly_review
from app.services.slack_service import decrypt_token, send_slack_message


def get_scheduled_users(db: Session) -> list[dict]:
    """
    Returns every user who has connected Slack AND enabled weekly
    notifications — the exact set n8n should loop over each Monday.
    """
    users = (
        db.query(User)
        .filter(User.slack_connected == True, User.slack_enabled == True)  # noqa: E712
        .all()
    )
    return [{"user_id": u.id, "email": u.email} for u in users]


def format_slack_message(review_result: dict) -> str:
    """
    Formats the generated literature review + references into a readable
    Slack message using Slack's mrkdwn formatting.
    """
    lines = ["📚 *Weekly Literature Review*", "", review_result["literature_review"]]

    references = review_result.get("references", [])
    if references:
        lines.append("")
        lines.append("*References*")
        for ref in references:
            lines.append(f"[{ref['citation']}] {ref['title']}")
            lines.append(ref["arxiv_url"])

    return "\n".join(lines)


def send_weekly_review_to_user(db: Session, user_id: int) -> dict:
    """
    Full per-user notification flow: generate that user's literature
    review (reusing the existing Fetcher -> Summarizer -> Critic ->
    Trend Analyst pipeline, unchanged), format it for Slack, and send it
    via their stored, encrypted bot token. Returns a success/failure
    dict rather than raising, so the API layer can report per-user
    outcomes without aborting a batch run over other users.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return {"success": False, "detail": "User not found."}

    if not user.slack_connected or not user.slack_enabled:
        return {"success": False, "detail": "User has not enabled Slack notifications."}

    try:
        review_result = generate_weekly_review(db, user_id)
        message = format_slack_message(review_result)
        bot_token = decrypt_token(user.slack_access_token)
        send_slack_message(bot_token, user.slack_user_id, message)
    except Exception as e:
        return {"success": False, "detail": str(e)}

    return {"success": True, "detail": "Review sent successfully."}