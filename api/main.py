from fastapi import FastAPI

from api.routes import router


app = FastAPI(
    title="AI App Builder API",
    description="API backend for the AI-powered App Development tool",
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "AI App Builder API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }