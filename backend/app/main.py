from fastapi import FastAPI

app = FastAPI(title="ANIA API")

@app.get("/health")
def health():
    return {"status": "ok"}
