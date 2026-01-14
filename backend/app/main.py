from fastapi import FastAPI
from app.routers import auth, deals, stages

app = FastAPI()
app.include_router(auth.router)
app.include_router(deals.router)
app.include_router(stages.router)
