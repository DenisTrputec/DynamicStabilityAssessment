from power_system.control_center import ControlCenter


class Bus:
    def __init__(self, number: int, name: str, base_voltage: float, bus_type: int, control_center: ControlCenter):
        self.number = number
        self.name = name
        self.base = base_voltage
        self.type = bus_type
        self.cc = control_center

    def __str__(self):
        return f"Bus: {self.number} {self.name}"

    property
    def info(self):
        return f"\nBus:" \
               f"\nNumber: {self.number}" \
               f"\nName: {self.name}" \
               f"\nBase Voltage: {self.base}" \
               f"\nCode Type: {self.type}" \
               f"\nControl Center: {self.cc.name}"


if __name__ == '__main__':
    b = Bus(10000, "Zagreb", 400.0, 1, ControlCenter.NDC)
    print(b.info)
