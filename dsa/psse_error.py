read = {
    0: None,
    1: "invalid NUMNAM value",
    2: "invalid revision number",
    3: "unable to convert file",
    4: "error opening temporary file",
    10: "error opening IFILE",
    11: "prerequisite requirements for API are not met"
}

readrawx = {
    0: None,
    2: "rawx read error",
    3: "error opening SFILE",
    4: "prerequisite requirements for API are not met"
}

case = {
    0: None,
    1: "SFILE is blank",
    2: "error reading from SFILE",
    3: "error opening SFILE",
    4: "prerequisite requirements for API are not met"
}

dyre_new = {
    0: None,
    1: "invalid STARTINDX value",
    3: "error opening output file",
    4: "prerequisite requirements for API are not met"
}

run = {
    0: None,
    1: "activity STRT needs to be executed",
    2: "invalid OPTION value",
    3: "generators are not converted",
    4: "error opening the current channel output file",
    5: "prerequisite requirements for API are not met"
}

dist_3phase_bus_fault = {
    0: None,
    1: "STRT or MSTR has not been successfully executed",
    2: "fixed bus shunt table is full",
    3: "bus is out-of-service",
    4: "invalid UNITS value",
    5: "invalid BASEKV value (<0.0)",
    6: "both BASEKV and the base voltage of bus IBUS are 0.0",
    7: "invalid bus number",
    8: "bus not found",
    9: "invalid node number",
    10: "bus does not belong to a substation",
    11: "node not found in the substation of this bus",
    12: "node is not connected to any bus section of this bus",
    13: "prerequisite requirements for API are not met"
}

dist_branch_fault = {
    0: None,
    1: "STRT or MSTR has not been successfully executed",
    2: "bus not found",
    3: "branch not found",
    4: "branch is out-of-service",
    5: "invalid UNITS value",
    6: "invalid BASEKV value (<0.0)",
    7: "both BASEKV and the base voltage of bus IBUS are 0.0",
    8: "prerequisite requirements for API are not met"
}

dist_clear_fault = {
    0: None,
    1: "STRT or MSTR not successfully executed",
    2: "bus not found",
    3: "branch not found",
    4: "three-winding transformer not found",
    5: "fixed bus shunt not found",
    6: "no faults in the fault memory tables",
    7: "invalid bus number",
    8: "bus not found",
    9: "invalid node number",
    10: "bus does not belong to a substation",
    11: "node not found in the substation of this bus",
    12: "node is not connected to any bus section of this bus",
    14: "prerequisite requirements for API are not met"
}

dist_branch_trip = {
    0: None,
    1: "STRT or MSTR has not been successfully executed",
    2: "bus not found",
    3: "branch not found",
    4: "branch is out-of-service",
    5: "prerequisite requirements for API are not met"
}

dist_branch_close = {
    0: None,
    1: "STRT or MSTR has not been successfully executed",
    2: "bus not found",
    3: "branch not found",
    4: "branch is already in-service",
    5: "bus is out-of-service",
    6: "prerequisite requirements for API are not met"
}

dist_bus_trip = {
    0: None,
    1: "STRT or MSTR not successfully executed",
    2: "bus not found",
    3: "bus is already disconnected",
    4: "prerequisite requirements for API are not met"
}

dist_machine_trip = {
    0: None,
    1: "STRT or MSTR not successfully executed",
    2: "bus not found",
    3: "machine not found",
    4: "machine is already in-service",
    5: "prerequisite requirements for API are not met"
}

strt_2 = {
    0: None,
    1: "generators are not converted",
    2: "invalid OPTIONS value",
    3: "prior initialization modified the loads - pick up original converted case",
    4: "error opening OUTFILE",
    5: "prerequisite requirements for API are not met",
}

voltage_channel = {
    0: None,
    1: "invalid STATUS value",
    2: "starting channel number is greater than the largest channel number allowed",
    3: "starting VAR index is greater than the largest VAR index allowed",
    4: "starting ICON index is greater than the largest ICON index allowed",
    5: "the maximum number of channel monitoring models has already been specified",
    6: "bus not found",
    7: "prerequisite requirements for API are not met"
}


branch_p_channel = {
    0: None,
    1: "invalid STATUS value",
    2: "starting channel number is greater than the largest channel number allowed",
    3: "starting VAR index is greater than the largest VAR index allowed",
    4: "starting ICON index is greater than the largest ICON index allowed",
    5: "model FLOW1 needs 3 ICONs but the last one exceeds the largest ICON index allowed",
    6: "the maximum number of channel monitoring models has already been specified",
    7: "bus not found",
    8: "branch not found",
    9: "prerequisite requirements for API are not met"
}
