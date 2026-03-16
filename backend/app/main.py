from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Smart Home Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}