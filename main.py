from fastapi import FastAPI
from routers import describe, insight

app = FastAPI()

app.include_router(describe.router)
app.include_router(insight.router)

@app.get("/")
def root():
    return {"message": "ETF API is running"}
