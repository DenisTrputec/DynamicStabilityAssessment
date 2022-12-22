from power_system.bus import Bus


class Generator:
    def __init__(self, bus: Bus, generator_id: str, status: int):
        self.bus = bus
        self.id = generator_id
        self.status = status

    def __str__(self):
        return f"Generator: {self.bus.number} {self.bus.name} {self.id}"

    def info(self):
        return f"\nGenerator:" \
               f"\nBus Number: {self.bus.number}" \
               f"\nBus Name: {self.bus.name}" \
               f"\nId: {self.id}" \
               f"\nControl Center: {self.bus.cc.name}" \
               f"\nStatus: {self.status}"
