from fastapi import FastAPI

from Task1.router import router as task1_router
from Task2.router import router as task2_router
from Task3.router import router as task3_router
from Task4.router import router as task4_router


app = FastAPI(title="Lang-Chain Testing")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(task1_router, tags=["Task 1"])

app.include_router(task2_router, tags=["Task 2"])

app.include_router(task3_router, tags=["Task 3"])

app.include_router(task4_router, tags=["Task 4"])