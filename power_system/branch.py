from power_system.bus import Bus


class Branch:
    def __init__(self, bus1: Bus, bus2: Bus, branch_id: str):
        self.bus1 = bus1
        self.bus2 = bus2
        self.id = branch_id
