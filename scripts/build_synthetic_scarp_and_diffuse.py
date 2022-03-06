import numpy as np

from scripts.utils.diffuse import diffuse
from config import config


def build_synthetic_scarp(fault_dip, fault_slip, fault_scarp_profile_length, number_of_fault_scarp_steps,
                          fault_step_width, fault_scarp_exponential):
    """
    Build a synthetic scarp profile
    :param fault_dip <int> The dip of the fault scarp in degrees
    :param fault_slip <int> The slip on the fault in meters
    :param fault_scarp_profile_length <int> The length of the profile in meters
    :param number_of_fault_scarp_steps <int> The number of steps in the scarp profile
    :param fault_step_width <string> The width of the steps between scarp profiles, in meters
    :param fault_scarp_exponential <boolean> The type of scarp profile, normal (False) or exponential (True)
    :return: scarp_profile_elevation <list> The elevation of the scarp profile
    """

    v = np.sin(np.deg2rad(fault_dip)) * fault_slip
    fault_scarp_width = np.cos(np.deg2rad(fault_dip)) * fault_slip
    v_dx = v / fault_scarp_width

    scarp_profile_elevation = np.zeros(fault_scarp_profile_length)

    for scarp_step in range(0, number_of_fault_scarp_steps):
        if scarp_step == 0:
            fault_scarp_start_location = round(
                (fault_scarp_profile_length / ((number_of_fault_scarp_steps + 1))) * (scarp_step + 1))
        else:
            fault_scarp_start_location = round((fault_scarp_profile_length / ((number_of_fault_scarp_steps + 1))) * (
                    scarp_step + 1)) + fault_step_width
        fault_scarp_end_location = round(fault_scarp_start_location + fault_scarp_width)
        for n in range(0, fault_scarp_profile_length):
            if n < fault_scarp_start_location:
                scarp_profile_elevation[n] += v
            elif fault_scarp_start_location <= n < fault_scarp_end_location:
                if fault_scarp_exponential:
                    scarp_profile_elevation[n] = scarp_profile_elevation[n - 1] - (
                            (1 / 2) ** ((n + 1) - fault_scarp_start_location)) * v
                else:
                    scarp_profile_elevation[n] = scarp_profile_elevation[n - 1] - v_dx
            elif n >= fault_scarp_end_location:
                scarp_profile_elevation[n] = scarp_profile_elevation[n]

    return scarp_profile_elevation


def build_synthetic_scarp_and_diffuse(config):
    scarp_profile_elevation = build_synthetic_scarp(config.fault_dip, config.fault_slip,
                                                    config.fault_scarp_profile_length, config.fault_scarp_steps,
                                                    config.fault_scarp_step_width, config.fault_scarp_exponential)

    diffuse(config.change_in_distance, scarp_profile_elevation, config.diffusion_coefficient,
            config.final_time, config.time_steps_between_plots, plot=True)



if __name__ == "__main__":
    build_synthetic_scarp_and_diffuse(config)
