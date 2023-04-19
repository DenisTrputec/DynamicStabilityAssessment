from power_system.control_center import ControlCenter


class Bus:
    def __init__(self, number: int, name: str, base_voltage: float, bus_type: int, area: int, zone: int):
        self.number = number
        self.name = name
        self.base = base_voltage
        self.type = bus_type
        self.area = area
        self.zone = zone

    def __str__(self):
        return f"{self.name}"

    @property
    def info(self):
        return f"\nBus:" \
               f"\nNumber: {self.number}" \
               f"\nName: {self.name}" \
               f"\nBase Voltage: {self.base}" \
               f"\nCode Type: {self.type}" \
               f"\nArea: {self.area}" \
               f"\nZone: {self.zone}"

    @property
    def full_name(self):
        return f"[{self.number}]{self.name}"

    @classmethod
    def load_from_json(cls, json_string):
        number = json_string["number"]
        name = json_string["name"]
        base = json_string["base"]
        bus_type = json_string["type"]
        area = json_string["area"]
        zone = json_string["zone"]
        instance = Bus(number, name, base, bus_type, area, zone)
        return instance


if __name__ == '__main__':
    b = Bus(10000, "Zagreb", 400.0, 1, 16, 11)
    print(b.info)
