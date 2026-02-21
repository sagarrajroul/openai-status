import httpx
import hashlib
import json

class ConditionalFetcher:
    def __init__(self, url):
        self.url = url
        self.last_hash = None

    async def fetch(self):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.url)

        response.raise_for_status()

        data = response.json()

        # Create stable hash of response
        payload_string = json.dumps(data, sort_keys=True)
        current_hash = hashlib.sha256(payload_string.encode()).hexdigest()

        if self.last_hash == current_hash:
            return None

        self.last_hash = current_hash
        return data