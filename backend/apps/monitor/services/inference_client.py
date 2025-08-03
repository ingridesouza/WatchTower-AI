import time

import httpx

INFERENCE_URL = "http://inference:8500/infer"


async def run_inference(file_bytes: bytes, filename: str = "frame.jpg"):
    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=20) as client:
        files = {"image": (filename, file_bytes, "image/jpeg")}
        r = await client.post(INFERENCE_URL, files=files)
        r.raise_for_status()
    latency_ms = int((time.perf_counter() - t0) * 1000)
    data = r.json()
    return data, latency_ms
