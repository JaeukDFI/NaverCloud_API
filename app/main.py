from fastapi import FastAPI
from routers import etf, insight

app = FastAPI()

app.include_router(etf.router)
app.include_router(insight.router)
