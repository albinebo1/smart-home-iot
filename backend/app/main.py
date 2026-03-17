from fastapi import FastAPI
from app.routes.rooms import router as rooms_router
from app.routes.system import router as system_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Smart Home Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(rooms_router)
app.include_router(system_router)