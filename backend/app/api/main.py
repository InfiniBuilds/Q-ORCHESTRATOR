from fastapi import FastAPI

from app.api.routes.orchestrator import router as orchestrator_router

app = FastAPI(
    title="Q-ORCHESTRATOR",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Q-ORCHESTRATOR Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }


app.include_router(
    orchestrator_router,
    tags=["Orchestrator"],
)
