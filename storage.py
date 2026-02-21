from datetime import datetime

class InMemoryStorage:
    def __init__(self):
        self.logs = []

    def save(self, product, status):
        self.logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product": product,
            "status": status
        })

    def get_all(self):
        return self.logs