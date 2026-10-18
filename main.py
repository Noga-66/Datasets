import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes_auth, routes_incidents, routes_ingest, websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    websocket.start_kafka_listener(asyncio.get_running_loop())
    yield


app = FastAPI(title="Ain Al-Madina AI", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"],
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(routes_auth.router)
app.include_router(routes_ingest.router)
app.include_router(routes_incidents.router)
app.include_router(websocket.router)


@app.get("/health")
def health():
    return {"status": "ok"}
