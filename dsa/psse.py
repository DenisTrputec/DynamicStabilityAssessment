import os
import sys
import json

from dsa import psse_error
from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine
from power_system.control_center import ControlCenter
from utils.logger import logger


with open('../config.json') as handle:
    config = json.load(handle)
    for key in config["psse"]:
        path = config["psse"][key]
        sys.path.append(path)
        os.environ['PATH'] = os.environ['PATH'] + ';' + path

import psspy
from psspy import _f


class PSSE:
    def __init__(self):
        pass

    @staticmethod
    def initialize(busses=50000):
        ierr = psspy.psseinit(busses)
        if ierr != 0:
            raise Exception(f"Couldn't initialize PSSE\tError Code:{ierr}")

    @staticmethod
    def read_raw(filepath):
        ierr = psspy.read(ifile=filepath)
        if ierr != 0:
            raise Exception(f"PSSE.read_raw: {psse_error.read[ierr]}")

    @staticmethod
    def read_dyr(filepath):
        ierr = psspy.dyre_new(dyrefile=filepath)
        if ierr != 0:
            raise Exception(f"PSSE.read_raw: {psse_error.dyre_new[ierr]}")

    @staticmethod
    def read_bus_data():
        _, (numbers, types, areas) = psspy.abusint(flag=2, string=["NUMBER", "TYPE", "AREA"])
        _, bases = psspy.abusreal(flag=2, string=["BASE"])
        _, names = psspy.abuschar(flag=2, string=["NAME"])
        bus_dict = {}
        for number, bus_type, cc_number, base_voltage, name in zip(numbers, types, areas, bases[0], names[0]):
            bus_dict[number] = Bus(number, name, base_voltage, bus_type, ControlCenter(cc_number))
        return bus_dict

    @staticmethod
    def read_branch_data(bus_dict=None):
        if not bus_dict:
            bus_dict = PSSE.read_bus_data()

        _, (from_numbers, to_numbers, statuses) = psspy.abrnint(flag=2, string=["FROMNUMBER", "TONUMBER", "STATUS"])
        _, branch_ids = psspy.abrnchar(flag=2, string=["ID"])

        branch_dict = {}
        for b1, b2, statuses, branch_id in zip(from_numbers, to_numbers, statuses, branch_ids[0]):
            branch_dict[(b1, b2, branch_id)] = Branch(bus_dict[b1], bus_dict[b2], branch_id, statuses)
        return branch_dict

    @staticmethod
    def read_machine_data(bus_dict=None):
        if not bus_dict:
            bus_dict = PSSE.read_bus_data()

        _, (bus_numbers, statuses) = psspy.amachint(flag=4, string=["NUMBER", "STATUS"])
        _, machine_ids = psspy.amachchar(flag=4, string=["ID"])

        machine_dict = {}
        for number, status, machine_id in zip(bus_numbers, statuses, machine_ids[0]):
            machine_dict[(number, machine_id)] = Machine(bus_dict[number], machine_id, status)
        return machine_dict

    @staticmethod
    def set_dynamic_parameters():
        psspy.dynamics_solution_param_2(realar=[_f, _f, 0.002, _f, _f, _f, _f, _f])
        psspy.set_relang(switch=1, ibusex=-1, id="")
        psspy.set_netfrq(status=1)

    @staticmethod
    def reset_plot_channels():
        psspy.delete_all_plot_channels()

    @staticmethod
    def simulation(time: float):
        logger.info(f"Simulation: {time}s]")
        ierr = psspy.run(tpause=time)
        return psse_error.run[ierr]

    @staticmethod
    def bus_fault(bus: Bus):
        logger.info(f"Bus Fault: {bus.name}")
        ierr = psspy.dist_3phase_bus_fault(ibus=bus.number)
        return psse_error.dist_3phase_bus_fault[ierr]

    @staticmethod
    def line_fault(branch: Branch):
        logger.info(f"Line Fault: {branch.name}")
        ierr = psspy.dist_branch_fault(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)
        return psse_error.dist_branch_fault[ierr]

    @staticmethod
    def clear_fault(index: int):
        logger.info(f"Clear Fault: {index}")
        ierr = psspy.dist_clear_fault(fault=index)
        return psse_error.dist_clear_fault[ierr]

    @staticmethod
    def line_trip(branch: Branch):
        logger.info(f"Line Trip: {branch.name}")
        ierr = psspy.dist_branch_trip(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)
        return psse_error.dist_branch_fault[ierr]

    @staticmethod
    def line_close(branch: Branch):
        logger.info(f"Line Close: {branch.name}")
        ierr = psspy.dist_branch_close(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)
        return psse_error.dist_branch_close[ierr]

    @staticmethod
    def bus_disconnect(bus: Bus):
        logger.info(f"Bus Disconnect: {bus.name}")
        ierr = psspy.dist_bus_trip(ibus=bus.number)
        return psse_error.dist_bus_trip[ierr]

    @staticmethod
    def machine_disconnect(machine: Machine):
        logger.info(f"Machine Disconnect: {machine.bus.name}")
        ierr = psspy.dist_machine_trip(ibus=machine.bus.number, id=machine.id)
        return psse_error.dist_machine_trip[ierr]

    method = {
        "simulation": simulation,
        "bus_fault": bus_fault,
        "line_fault": line_fault,
        "clear_fault": clear_fault,
        "line_trip": line_trip,
        "line_close": line_close,
        "bus_disconnect": bus_disconnect,
        "machine_disconnect": machine_disconnect
    }

    @staticmethod
    def initialize_output(output_filepath: str):
        logger.info(f"Initialize output file: {output_filepath}")
        psspy.cong(0)
        psspy.conl(0, 1, 1, [0, 0], [100.0, 0.0, 0.0, 100.0])
        psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
        psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, 0.0, 100.0])
        psspy.ordr(0)
        psspy.fact()
        psspy.tysl(0)
        ierr = psspy.strt_2(options=[0, 0], outfile=output_filepath)
        return psse_error.strt_2[ierr]

    @staticmethod
    def add_voltage_channel(bus: Bus):
        logger.info(f"Add Voltage Channel for Bus: {bus.name}")
        ierr = psspy.voltage_channel(status=[-1, -1, -1, bus.number], ident=bus.name[:8])
        return psse_error.voltage_channel[ierr]


if __name__ == '__main__':
    PSSE.initialize()
    PSSE.read_raw(r"""E:\Python3\DynamicStabilityAssessment\input_files\S10_final_converted.raw""")
    PSSE.read_dyr(r"""E:\Python3\DynamicStabilityAssessment\input_files\DINAMIKA_KOMPLET.dyr""")
    PSSE.set_dynamic_parameters()
    PSSE.initialize_output(r"""E:\Python3\DynamicStabilityAssessment\output\S10\temp.outx""")
    PSSE.method["simulation"](1.0)
