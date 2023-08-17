import config
import uvicorn
from fastapi import FastAPI
from views import stations_router

app = FastAPI()
app.include_router(stations_router, prefix="/api/stations")


@app.get("/health")
def health():
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
