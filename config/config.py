# Synthetic fault scarp parameters
fault_dip = 60
fault_slip = 10
fault_slip_rate = 2
fault_scarp_profile_length = 30
fault_scarp_exponential = True # True for simple
fault_scarp_steps = 1
fault_scarp_step_width = 5
final_time = fault_slip / fault_slip_rate

# Parameters for synthetic fault scarps and for calculating diffusion age from real scarps
diffusion_coefficient = 10 # diffusion coefficient in mm per year
time_steps_between_plots = 20
change_in_distance = 1
calculation_final_time = 25 # Final time in kyr