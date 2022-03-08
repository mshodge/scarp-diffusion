import pytest
from scripts.build_synthetic_scarp_and_diffuse import build_synthetic_scarp


def test_build_simple():
    fault_dip = 60
    fault_slip = 10
    fault_slip_rate = 2
    fault_scarp_profile_length = 30
    fault_scarp_exponential = False  # True for simple
    fault_scarp_steps = 1
    fault_scarp_step_width = 5
    final_time = fault_slip / fault_slip_rate

    scarp_profile_elevation = build_synthetic_scarp(fault_dip, fault_slip,
                                                    fault_scarp_profile_length, fault_scarp_steps,
                                                    fault_scarp_step_width, fault_scarp_exponential)

    scarp_profile_elevation_int = [int(elem) for elem in scarp_profile_elevation]

    assert scarp_profile_elevation_int == [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 5, 3, 1, 0, 0, 0, 0, 0, 0,
                                           0, 0, 0, 0, 0]

def test_build_exponential():
    fault_dip = 60
    fault_slip = 10
    fault_slip_rate = 2
    fault_scarp_profile_length = 30
    fault_scarp_exponential = True  # True for simple
    fault_scarp_steps = 1
    fault_scarp_step_width = 5
    final_time = fault_slip / fault_slip_rate

    scarp_profile_elevation = build_synthetic_scarp(fault_dip, fault_slip,
                                                    fault_scarp_profile_length, fault_scarp_steps,
                                                    fault_scarp_step_width, fault_scarp_exponential)

    scarp_profile_elevation_int = [int(elem) for elem in scarp_profile_elevation]

    assert scarp_profile_elevation_int == [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0,
                                           0, 0, 0, 0, 0]


def test_build_steps():
    fault_dip = 60
    fault_slip = 10
    fault_slip_rate = 2
    fault_scarp_profile_length = 30
    fault_scarp_exponential = False  # True for simple
    fault_scarp_steps = 3
    fault_scarp_step_width = 5
    final_time = fault_slip / fault_slip_rate

    scarp_profile_elevation = build_synthetic_scarp(fault_dip, fault_slip,
                                                    fault_scarp_profile_length, fault_scarp_steps,
                                                    fault_scarp_step_width, fault_scarp_exponential)

    scarp_profile_elevation_int = [int(elem) for elem in scarp_profile_elevation]

    assert scarp_profile_elevation_int == [25, 25, 25, 25, 25, 25, 25, 25, 24, 22, 20, 19, 17, 17, 17, 17, 17, 17,
                                           17, 17, 15, 13, 12, 10, 8, 8, 8, 6, 5, 3]


