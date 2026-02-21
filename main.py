import asyncio
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

async def main():
    event_bus = EventBus()
    storage = InMemoryStorage()
    processor = IncidentProcessor(storage)

    schedulers = [
        ProviderScheduler(provider, event_bus)
        for provider in PROVIDERS
    ]

    await asyncio.gather(
        *(scheduler.run() for scheduler in schedulers),
        event_bus.consume(processor.handle)
    )

if __name__ == "__main__":
    asyncio.run(main())