from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="WatchTower AI Inference", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/infer")
async def infer(image: UploadFile = File(...)):
    content = await image.read()
    _ = len(content)
    return {"model": "stub", "detections": []}
