from app.api.content_endpoint import router as content_router
from app.api.pricing_endpoint import router as pricing_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(content_router, prefix="", tags=["Content Router"])
app.include_router(pricing_router, prefix="", tags=["Pricing Router"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)