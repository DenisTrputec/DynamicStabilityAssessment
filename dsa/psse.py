import os
import sys
import json

from dsa import psse_error
from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine
from utils.logger import logger


with open('config.json') as handle:
    config = json.load(handle)
    for key in config["psse"]:
        path = config["psse"][key]
        sys.path.append(path)
        os.environ['PATH'] = os.environ['PATH'] + ';' + path

import psspy
from psspy import _f
import dyntools
import redirect
redirect.psse2py()


def initialize(busses=50000) -> str:
    ierr = psspy.psseinit(busses)
    if ierr != 0:
        return f"Couldn't initialize PSSE\tError Code:{ierr}"


def read_model_file(filepath: str) -> str:
    logger.info(f"Read model file: {filepath}")
    if filepath.lower().endswith(".raw"):
        return psse_error.read[psspy.read(ifile=filepath)]
    elif filepath.lower().endswith(".rawx"):
        return psse_error.readrawx[psspy.readrawx(sfile=filepath)]
    else:
        return psse_error.case[psspy.case(sfile=filepath)]


def read_dynamics_file(filepath: str) -> str:
    logger.info(f"Read dynamics file: {filepath}")
    return psse_error.dyre_new[psspy.dyre_new(dyrefile=filepath)]


def read_bus_data(filters: dict = None) -> dict:
    logger.info("")
    err1, (numbers, types, areas, zones) = psspy.abusint(flag=2, string=["NUMBER", "TYPE", "AREA", "ZONE"])
    err2, bases = psspy.abusreal(flag=2, string=["BASE"])
    err3, names = psspy.abuschar(flag=2, string=["NAME"])

    if any([err1, err2, err3]):
        return {}

    bus_dict = {}
    for number, bus_type, area, zone, base_voltage, name in zip(numbers, types, areas, zones, bases[0], names[0]):
        if filters:
            for k, values in filters.items():
                if k == "area" and area in values:
                    bus_dict[number] = Bus(number, name, base_voltage, bus_type, area, zone)
        else:
            bus_dict[number] = Bus(number, name, base_voltage, bus_type, area, zone)
    return bus_dict


def read_branch_data(bus_dict=None, filters: dict = None) -> dict:
    logger.info("")
    if not bus_dict:
        bus_dict = read_bus_data()

    err1, (from_numbers, to_numbers, statuses) = psspy.abrnint(flag=2, string=["FROMNUMBER", "TONUMBER", "STATUS"])
    err2, branch_ids = psspy.abrnchar(flag=2, string=["ID"])

    if any([err1, err2]):
        return {}

    branch_dict = {}
    for b1, b2, statuses, branch_id in zip(from_numbers, to_numbers, statuses, branch_ids[0]):
        bus1 = bus_dict[b1]
        bus2 = bus_dict[b2]
        if filters:
            for k, values in filters.items():
                if k == "area" and (bus1.area in values or bus2.area in values):
                    branch_dict[(b1, b2, branch_id)] = Branch(bus1, bus2, branch_id, statuses)
        else:
            branch_dict[(b1, b2, branch_id)] = Branch(bus1, bus2, branch_id, statuses)
    return branch_dict


def read_machine_data(bus_dict=None) -> dict:
    logger.info("")
    if not bus_dict:
        bus_dict = read_bus_data()

    err1, (bus_numbers, statuses, modes) = psspy.amachint(flag=4, string=["NUMBER", "STATUS", "WMOD"])
    err2, machine_ids = psspy.amachchar(flag=4, string=["ID"])

    if any([err1, err2]):
        return {}

    machine_dict = {}
    for number, status, mode, machine_id in zip(bus_numbers, statuses, modes, machine_ids[0]):
        machine_dict[(number, machine_id)] = Machine(bus_dict[number], machine_id, status, mode)
    return machine_dict


def set_dynamic_parameters(simulation_time_step: float = 0.002):
    logger.info(f"")
    psspy.dynamics_solution_param_2(realar=[_f, _f, simulation_time_step, _f, _f, _f, _f, _f])
    psspy.set_relang(switch=1, ibusex=-1, id="")
    psspy.set_netfrq(status=1)


def convert_model():
    logger.info(f"")
    psspy.cong(0)
    psspy.conl(0, 1, 1, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.ordr(0)
    psspy.fact()
    psspy.tysl(0)


def reset_plot_channels():
    logger.info("")
    psspy.delete_all_plot_channels()


def initialize_output(output_filepath: str):
    logger.info(f"Initialize output file: {output_filepath}")
    return psse_error.strt_2[psspy.strt_2(options=[0, 0], outfile=output_filepath)]


def add_bus_u_channel(bus: Bus):
    logger.info(f"Add Voltage Channel for Bus: {bus.name}")
    return psse_error.voltage_channel[psspy.voltage_channel(status=[-1, -1, -1, bus.number], ident=bus.name)]


def add_branch_p_channel(branch: Branch):
    logger.info(f"Add Voltage Channel for Bus: {branch.name}")
    return psse_error.branch_p_channel[
        psspy.branch_p_channel(status=[-1, -1, -1, branch.bus1.number, branch.bus2.number],
                               id=branch.id, ident=branch.name)]


def save_output(out_filepath: str, save_filepath: str):
    logger.info(f"Save output file: {out_filepath}")
    output_obj = dyntools.CHNF(out_filepath)
    output_obj.csvout(csvfile=save_filepath)
    return


def simulation(time: float):
    logger.info(f"Simulation: {time}s]")
    return psse_error.run[psspy.run(tpause=time)]


def bus_fault(bus: Bus):
    logger.info(f"Bus Fault: {bus.name}")
    return psse_error.dist_3phase_bus_fault[psspy.dist_3phase_bus_fault(ibus=bus.number)]


def line_fault(branch: Branch):
    logger.info(f"Line Fault: {branch.name}")
    ierr = psspy.dist_branch_fault(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)
    return psse_error.dist_branch_fault[ierr]


def clear_fault(index: int):
    logger.info(f"Clear Fault: {index}")
    return psse_error.dist_clear_fault[psspy.dist_clear_fault(fault=index)]


def line_trip(branch: Branch):
    logger.info(f"Line Trip: {branch.name}")
    ierr = psspy.dist_branch_trip(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)
    return psse_error.dist_branch_fault[ierr]


def line_close(branch: Branch):
    logger.info(f"Line Close: {branch.name}")
    ierr = psspy.dist_branch_close(ibus=branch.bus1.number, jbus=branch.bus2.number, id=branch.id)
    return psse_error.dist_branch_close[ierr]


def bus_disconnect(bus: Bus):
    logger.info(f"Bus Disconnect: {bus.name}")
    return psse_error.dist_bus_trip[psspy.dist_bus_trip(ibus=bus.number)]


def machine_disconnect(machine: Machine):
    logger.info(f"Machine Disconnect: {machine.bus.name}")
    return psse_error.dist_machine_trip[psspy.dist_machine_trip(ibus=machine.bus.number, id=machine.id)]


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


if __name__ == '__main__':
    initialize()
    read_model_file(r"""E:\Python3\DynamicStabilityAssessment\input_files\S10_final.raw""")
    read_dynamics_file(r"""E:\Python3\DynamicStabilityAssessment\input_files\DINAMIKA_KOMPLET.dyr""")
    bus_data = read_bus_data()
    read_branch_data(bus_data)
    read_machine_data(bus_data)
    set_dynamic_parameters()
    convert_model()
    for b in bus_data.values():
        add_bus_u_channel(b)

    initialize_output(r"""E:\Python3\DynamicStabilityAssessment\output\temp.out""")
    simulation(1)
    save_output(r"""E:\Python3\DynamicStabilityAssessment\output\temp.out""", r"""E:\Python3\DynamicStabilityAssessment\output\temp.csv""")
