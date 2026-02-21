import asyncio
import os
from fastapi import FastAPI
import uvicorn

from event_bus import EventBus
from storage import InMemoryStorage
from processor import IncidentProcessor
from scheduler import ProviderScheduler



PROVIDERS = [
    {
        "name": "OpenAI API",
        "url": "https://status.openai.com/api/v2/incidents.json",
        "interval": 30
    }
]

app = FastAPI()

# Global references
event_bus = EventBus()
storage = InMemoryStorage()
processor = IncidentProcessor(storage)
background_tasks = []

@app.get("/logs")
async def get_logs():
    return storage.get_all()

@app.get("/")
async def health():
    return {"status": "monitor running"}


async def start_monitoring():
    schedulers = [
        ProviderScheduler(provider, event_bus)
        for provider in PROVIDERS
    ]

    await asyncio.gather(
        *(scheduler.run() for scheduler in schedulers),
        event_bus.consume(processor.handle)
    )


@app.on_event("startup")
async def startup_event():
    # Run monitor as background task
    task = asyncio.create_task(start_monitoring())
    background_tasks.append(task)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


