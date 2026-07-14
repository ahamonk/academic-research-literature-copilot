from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth

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


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}