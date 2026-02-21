from datetime import datetime

class IncidentProcessor:
    def __init__(self, storage):
        self.storage = storage

    async def handle(self, event):
        try:
            # 1️⃣ Format timestamp
            raw_time = event.get("updated_at")
            if raw_time:
                dt = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Since components not present, use page + incident name structure
            product = f"OpenAI API"

            latest_update =event.get('name', 'Unknown Service')

            # latest_update = None
            # for update in reversed(updates):
            #     body = update.get("body")
            #     if body and body.strip():
            #         latest_update = body.strip()
            #         break

            # if not latest_update:
            #     latest_update = event.get("status", "No details available")

            # Save
            self.storage.save(product, latest_update)

            # Print in required format
            print(f"[{timestamp}] Product: {product}")
            print(f"Status: {latest_update}")
            print("=" * 60)

        except Exception as e:
            print("Processing error:", e)