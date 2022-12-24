import os
import sys

import psse_errors
from power_system.bus import Bus
from power_system.control_center import ControlCenter

PSSE_PATH = r"C:\Instalacije\PTI\PSSE35\35.3\PSSBIN"
PSSPY_PATH = r"C:\Instalacije\PTI\PSSE35\35.3\PSSPY37"

for PATH in [PSSE_PATH, PSSPY_PATH]:
    sys.path.append(PATH)
    os.environ['PATH'] = os.environ['PATH'] + ';' + PATH

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
    def read_busses():
        _, (numbers, types, areas) = psspy.abusint(flag=2, string=["NUMBER", "TYPE", "AREA"])
        _, bases = psspy.abusreal(flag=2, string=["BASE"])
        _, names = psspy.abuschar(flag=2, string=["NAME"])

        bus_list = []
        for number, bus_type, cc_number, base_voltage, name in zip(numbers, types, areas, bases[0], names[0]):
            bus_list.append(Bus(number, name, base_voltage, bus_type, ControlCenter(cc_number)))
        return bus_list


if __name__ == '__main__':
    PSSE.initialize()
    try:
        PSSE.read_raw(r"D:\Programi\DynamicStabilityAssessment\input_data\sample.raw")
    except Exception as e:
        print(e)
    buses = PSSE.read_busses()
    for bus in buses:
        print(bus, bus.cc.name)