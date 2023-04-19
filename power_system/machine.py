from power_system.bus import Bus


class Machine:
    def __init__(self, bus: Bus, machine_id: str, status: int):
        self.bus = bus
        self.id = machine_id
        self.status = status

    def __str__(self):
        return f"{self.bus.name}/{self.id}"

    def info(self):
        return f"\nMachine:" \
               f"\nBus Number: {self.bus.number}" \
               f"\nBus Name: {self.bus.name}" \
               f"\nId: {self.id}" \
               f"\nControl Center: {self.bus.area}" \
               f"\nStatus: {self.status}"

    @property
    def name(self):
        return f"{self.bus.name}/{self.id}"

    @property
    def full_name(self):
        return f"[{self.bus.number}]{self.bus.name}/{self.id}"

    @classmethod
    def load_from_json(cls, json_string):
        bus = Bus.load_from_json(json_string["bus"])
        machine_id = json_string["id"]
        status = json_string["status"]
        instance = Machine(bus, machine_id, status)
        return instance
