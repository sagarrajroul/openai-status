import asyncio
from monitor import ConditionalFetcher
from detector import IncidentDetector

class ProviderScheduler:
    def __init__(self, provider, event_bus):
        self.provider = provider
        self.fetcher = ConditionalFetcher(provider["url"])
        self.detector = IncidentDetector()
        self.event_bus = event_bus

    async def run(self):
        while True:
            try:
                data = await self.fetcher.fetch()
                if data:
                    incidents = data.get("incidents", [])
                    new_events = self.detector.detect(incidents)

                    for event in new_events:
                        await self.event_bus.publish(event)

            except Exception as e:
                print(f"Error in {self.provider['name']}:", e)

            await asyncio.sleep(self.provider["interval"])