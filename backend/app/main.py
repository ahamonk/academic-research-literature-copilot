from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, papers, search, topics, clusters
from app.database import SessionLocal, run_startup_migrations
from app.services.topic_service import seed_topics

app = FastAPI(
    title="Academic Research Trend and Literature Review Copilot",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(papers.router)
app.include_router(search.router)
app.include_router(topics.router)
app.include_router(clusters.router)


@app.on_event("startup")
def on_startup():
    run_startup_migrations()
    db = SessionLocal()
    try:
        seed_topics(db)
    finally:
        db.close()


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}