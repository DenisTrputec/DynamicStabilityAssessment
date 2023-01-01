from power_system.bus import Bus


class Branch:
    def __init__(self, bus1: Bus, bus2: Bus, branch_id: str, status: int):
        self.bus1 = bus1
        self.bus2 = bus2
        self.id = branch_id
        self.status = status

    def __str__(self):
        return f"{self.bus1.name}-{self.bus2.name}/{self.id}"

    @property
    def info(self):
        return f"\nBranch:" \
               f"\nBus 1 Number: {self.bus1.number}" \
               f"\nBus 1 Name: {self.bus1.name}" \
               f"\nBus 2 Number: {self.bus2.number}" \
               f"\nBus 2 Name: {self.bus2.name}" \
               f"\nId: {self.id}" \
               f"\nControl Center 1: {self.bus1.cc.name}" \
               f"\nControl Center 2: {self.bus2.cc.name}" \
               f"\nStatus: {self.status}"

    @property
    def name(self):
        return f"{self.bus1.name}-{self.bus2.name}/{self.id}"

    @property
    def full_name(self):
        return f"[{self.bus1.number}]{self.bus1.name}-[{self.bus2.number}]{self.bus2.name}/{self.id}"

    @classmethod
    def load_from_json(cls, json_string):
        bus1 = Bus.load_from_json(json_string["bus1"])
        bus2 = Bus.load_from_json(json_string["bus2"])
        branch_id = json_string["id"]
        status = json_string["status"]
        instance = Branch(bus1, bus2, branch_id, status)
        return instance
