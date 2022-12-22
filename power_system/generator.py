from power_system.bus import Bus


class Generator:
    def __init__(self, bus: Bus, generator_id: str):
        self.bus = bus
        self.id = generator_id
