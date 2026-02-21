class IncidentDetector:
    def __init__(self):
        self.state = {}

    def detect(self, incidents):
        new_events = []

        for inc in incidents:
            key = inc["id"]
            updated = inc["updated_at"]

            if key not in self.state or self.state[key] != updated:
                self.state[key] = updated
                new_events.append(inc)

        return new_events