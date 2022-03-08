import pytest
from scripts.build_synthetic_scarp_and_diffuse import build_synthetic_scarp
from scripts.utils.diffuse import diffuse


def test_diffusion():
    fault_dip = 60
    fault_slip = 10
    fault_slip_rate = 2
    fault_scarp_profile_length = 30
    fault_scarp_exponential = False  # True for simple
    fault_scarp_steps = 1
    fault_scarp_step_width = 5
    final_time = fault_slip / fault_slip_rate
    diffusion_coefficient = 10  # diffusion coefficient in mm per year
    change_in_distance = 1
    time_steps_between_plots = 20

    scarp_profile_elevation = build_synthetic_scarp(fault_dip, fault_slip,
                                                    fault_scarp_profile_length, fault_scarp_steps,
                                                    fault_scarp_step_width, fault_scarp_exponential)

    diffused_profile = diffuse(change_in_distance, scarp_profile_elevation, diffusion_coefficient,
            final_time, time_steps_between_plots, plot=False)

    diffused_scarp_profile_elevation_int = [int(elem) for elem in diffused_profile[0][-1]]

    assert diffused_scarp_profile_elevation_int == [8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2,
                                                    2, 2, 2, 2, 1, 1, 1, 1]
