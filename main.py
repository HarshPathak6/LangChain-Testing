from fastapi import FastAPI

from Task1.router import router as task1_router

app = FastAPI(title="Lang-Chain Testing")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(task1_router, tags=["Task 1"])
