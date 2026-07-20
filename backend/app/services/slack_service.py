import requests
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User

SLACK_AUTHORIZE_URL = "https://slack.com/oauth/v2/authorize"
SLACK_TOKEN_URL = "https://slack.com/api/oauth.v2.access"

# Bot scopes needed to open a DM with the connecting user and post messages.
SLACK_BOT_SCOPES = "chat:write,im:write,users:read"


def _get_fernet():
    from cryptography.fernet import Fernet

    if not settings.slack_token_encryption_key:
        raise RuntimeError(
            "SLACK_TOKEN_ENCRYPTION_KEY is not set. Add it to your .env "
            "file to use Slack integration."
        )
    return Fernet(settings.slack_token_encryption_key.encode())


def encrypt_token(token: str) -> str:
    """Encrypt a Slack access token before storing it in PostgreSQL."""
    return _get_fernet().encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt a stored Slack access token for use when calling the Slack API."""
    return _get_fernet().decrypt(encrypted_token.encode()).decode()


def build_authorize_url(state: str) -> str:
    """
    Build the Slack OAuth authorization URL the user's browser should be
    sent to. `state` embeds the requesting user's identity (a signed JWT,
    reusing the existing auth_service token utilities) so the callback -
    which Slack calls directly, outside any authenticated frontend
    session - can identify which user just connected Slack.
    """
    if not settings.slack_client_id or not settings.slack_redirect_uri:
        raise RuntimeError(
            "SLACK_CLIENT_ID and SLACK_REDIRECT_URI must be set in .env "
            "to use Slack integration."
        )

    return (
        f"{SLACK_AUTHORIZE_URL}"
        f"?client_id={settings.slack_client_id}"
        f"&scope={SLACK_BOT_SCOPES}"
        f"&redirect_uri={settings.slack_redirect_uri}"
        f"&state={state}"
    )


def exchange_code_for_token(code: str) -> dict:
    """
    Exchange the OAuth authorization code Slack sent back for an actual
    bot access token, workspace info, and the connecting user's Slack
    user ID.
    """
    if not settings.slack_client_id or not settings.slack_client_secret:
        raise RuntimeError("SLACK_CLIENT_ID and SLACK_CLIENT_SECRET must be set in .env.")

    response = requests.post(
        SLACK_TOKEN_URL,
        data={
            "client_id": settings.slack_client_id,
            "client_secret": settings.slack_client_secret,
            "code": code,
            "redirect_uri": settings.slack_redirect_uri,
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(f"Slack OAuth exchange failed: {data.get('error')}")

    return data


def save_slack_connection(db: Session, user: User, token_data: dict) -> None:
    """
    Persist the Slack connection on the user's row: encrypted bot token,
    workspace info, and the connecting user's Slack user ID (needed to
    open a DM channel later). Weekly notifications are enabled by
    default on connect; the user can turn them off via the toggle.
    """
    access_token = token_data["access_token"]
    team = token_data.get("team", {})
    authed_user = token_data.get("authed_user", {})

    user.slack_access_token = encrypt_token(access_token)
    user.slack_workspace_id = team.get("id")
    user.slack_workspace_name = team.get("name")
    user.slack_user_id = authed_user.get("id")
    user.slack_connected = True
    user.slack_enabled = True

    db.commit()


def disconnect_slack(db: Session, user: User) -> None:
    """Remove all stored Slack connection data for this user."""
    user.slack_access_token = None
    user.slack_workspace_id = None
    user.slack_workspace_name = None
    user.slack_user_id = None
    user.slack_connected = False
    user.slack_enabled = False

    db.commit()


def set_slack_enabled(db: Session, user: User, enabled: bool) -> None:
    """Toggle whether this user receives weekly Slack notifications."""
    user.slack_enabled = enabled
    db.commit()


def send_slack_message(bot_token: str, slack_user_id: str, text: str) -> None:
    """
    Send a direct message to the given Slack user, using the workspace's
    bot token. Slack requires opening a DM channel first — you can't
    post directly to a user ID as if it were a channel.
    """
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    client = WebClient(token=bot_token)

    try:
        im_response = client.conversations_open(users=[slack_user_id])
        channel_id = im_response["channel"]["id"]
        client.chat_postMessage(channel=channel_id, text=text)
    except SlackApiError as e:
        raise RuntimeError(f"Slack API error: {e.response['error']}")