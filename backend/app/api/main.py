from app.api.routes.iot.router import router as iot_router
from app.api.routes.banking.router import router as banking_router
from fastapi import FastAPI
from app.api.routes.analytics import router as analytics_router
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

app.include_router(analytics_router)
app.include_router(
    orchestrator_router,
    tags=["Orchestrator"],
)
app.include_router(
    banking_router,
)
app.include_router(
    iot_router,
)

