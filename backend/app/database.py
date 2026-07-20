from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_startup_migrations():
    """
    Minimal, additive-only schema patches — adds new columns if they
    don't already exist. Not a full migration system (no Alembic);
    appropriate for a fast-moving academic project with a small,
    evolving schema.
    """
    with engine.begin() as conn:
        conn.execute(
            text("ALTER TABLE topics ADD COLUMN IF NOT EXISTS discipline VARCHAR(100)")
        )
        conn.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS slack_connected BOOLEAN NOT NULL DEFAULT FALSE")
        )
        conn.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS slack_enabled BOOLEAN NOT NULL DEFAULT FALSE")
        )
        conn.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS slack_access_token VARCHAR")
        )
        conn.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS slack_workspace_id VARCHAR")
        )
        conn.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS slack_workspace_name VARCHAR")
        )
        conn.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS slack_user_id VARCHAR")
        )