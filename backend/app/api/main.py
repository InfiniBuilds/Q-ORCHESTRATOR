from fastapi import FastAPI

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
