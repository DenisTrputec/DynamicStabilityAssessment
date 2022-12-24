from power_system.bus import Bus


class Machine:
    def __init__(self, bus: Bus, machine_id: str, status: int):
        self.bus = bus
        self.id = machine_id
        self.status = status

    def __str__(self):
        return f"Machine: {self.bus.number} {self.bus.name} {self.id}"

    def info(self):
        return f"\nMachine:" \
               f"\nBus Number: {self.bus.number}" \
               f"\nBus Name: {self.bus.name}" \
               f"\nId: {self.id}" \
               f"\nControl Center: {self.bus.cc.name}" \
               f"\nStatus: {self.status}"