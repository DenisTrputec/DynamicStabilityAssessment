import os
import sys
import json

from dsa import psse_errors
from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine
from power_system.control_center import ControlCenter


with open('config.json') as handle:
    config = json.load(handle)
    for key in config["psse"]:
        path = config["psse"][key]
        sys.path.append(path)
        os.environ['PATH'] = os.environ['PATH'] + ';' + path

import psspy


class PSSE:
    def __init__(self):
        pass

    @staticmethod
    def initialize(busses=10000):
        ierr = psspy.psseinit(busses)
        if ierr != 0:
            raise Exception(f"Couldn't initialize PSSE\tError Code:{ierr}")

    @staticmethod
    def read_raw(filepath):
        ierr = psspy.read(ifile=filepath)
        if ierr != 0:
            raise Exception(f"PSSE.read_raw: {psse_errors.read[ierr]}")

    @staticmethod
    def __find_bus(bus_list, bus_number1, bus_number2=None):
        bus1 = None
        bus2 = None
        flag1 = False
        flag2 = True if bus_number2 else False

        for bus in bus_list:
            if bus.number == bus_number1:
                bus1 = bus
            elif bus.number == bus_number2:
                bus2 = bus
            if flag1 and flag2:
                break

        if not bus2:
            return bus1
        else:
            return bus1, bus2

    @staticmethod
    def read_busses():
        _, (numbers, types, areas) = psspy.abusint(string=["NUMBER", "TYPE", "AREA"])
        _, bases = psspy.abusreal(string=["BASE"])
        _, names = psspy.abuschar(string=["NAME"])

        bus_list = []
        for number, bus_type, cc_number, base_voltage, name in zip(numbers, types, areas, bases[0], names[0]):
            bus_list.append(Bus(number, name, base_voltage, bus_type, ControlCenter(cc_number)))
        return bus_list

    @staticmethod
    def read_branches(bus_list=None):
        if not bus_list:
            bus_list = PSSE.read_busses()

        _, (from_numbers, to_numbers, statuses) = psspy.abrnint(string=["FROMNUMBER", "TONUMBER", "STATUS"])
        _, branch_ids = psspy.abrnchar(string=["ID"])

        branch_list = []
        for b1, b2, statuses, branch_id in zip(from_numbers, to_numbers, statuses, branch_ids[0]):
            bus1, bus2 = PSSE.__find_bus(bus_list, b1, b2)
            branch_list.append(Branch(bus1, bus2, branch_id, statuses))
        return branch_list

    @staticmethod
    def read_machines(bus_list=None):
        if not bus_list:
            bus_list = PSSE.read_busses()

        _, (bus_numbers, statuses) = psspy.amachint(string=["NUMBER", "STATUS"])
        _, machine_ids = psspy.amachchar(string=["ID"])

        machine_list = []
        for number, status, machine_id in zip(bus_numbers, statuses, machine_ids[0]):
            bus = PSSE.__find_bus(bus_list, number)
            machine_list.append(Machine(bus, machine_id, status))
        return machine_list

    @staticmethod
    def simulation(time: float):
        print(f"Simulation: {time}s]")
        # ierr = psspy.run(tpause=time)

    @staticmethod
    def bus_fault(bus: Bus):
        print(f"Bus Fault: {bus.name}")
        # ierr = psspy.dist_3phase_bus_fault(ibus=bus.number)

    @staticmethod
    def line_fault(branch: Branch):
        print(f"Line Fault: {branch.name}")
        # ierr = psspy.dist_branch_fault(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)

    @staticmethod
    def clear_fault(index: int):
        print(f"Clear Fault: {index}")
        # ierr = psspy.dist_clear_fault(fault=index)

    @staticmethod
    def line_trip(branch: Branch):
        print(f"Line Trip: {branch.name}")
        # ierr = psspy.dist_branch_trip(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)

    @staticmethod
    def line_close(branch: Branch):
        print(f"Line Close: {branch.name}")
        # ierr = psspy.dist_branch_close(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)

    @staticmethod
    def bus_disconnect(bus: Bus):
        print(f"Bus Disconnect: {bus.name}")
        # ierr = psspy.dist_bus_trip(ibus=bus.number)

    @staticmethod
    def machine_disconnect(machine: Machine):
        print(f"Machine Disconnect: {machine.bus.name}")
        # ierr = psspy.dist_bus_trip(ibus=machine.bus.number)


if __name__ == '__main__':
    PSSE.initialize()
    try:
        PSSE.read_raw(r"D:\Programiranje\Moje aplikacije\Python\DynamicStabilityAssessment\input_files\sample.raw")
    except Exception as e:
        print(e)
    buses = PSSE.read_busses()
    branches = PSSE.read_branches()
    machines = PSSE.read_machines()
    for m in machines:
        print(m)
