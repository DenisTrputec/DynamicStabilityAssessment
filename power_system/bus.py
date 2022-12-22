from power_system.control_center import ControlCenter


class Bus:
    def __init__(self, number: int, name: str, base_voltage: float, bus_type: int, control_center: ControlCenter):
        self.number = number
        self.name = name
        self.base = base_voltage
        self.type = bus_type
        self.cc = control_center
