import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from operator import add
import time

from scripts.utils.slope import find_slope





def diffuse(change_in_distance, scarp_profile_elevation, diffusion_coefficient, final_time, time_steps_between_plots,
			plot = False):
	"""
	Performs the diffusion calculation on a scarp profile
	:param change_in_distance: <int> The change in distance between points on the scarp profile
	:param scarp_profile_elevation: <list> The elevation values along the scarp profile
	:param diffusion_coefficient: <int> The diffusion coefficient in mm per year
	:param final_time: <int> The final time in kyrs to calculate for
	:param time_steps_between_plots: <int> The time steps between output plots
	:param plot: <boolean> Whether or not to plot the profiles at time_steps_between_plots
	:return elevation_after_diffusion: <list> The elevation after the diffusion
	:return slope_after_diffusion: <list> The slope after the diffusion
	:return time_after_diffusion: <list> The time after the diffusion
	"""
	if plot:
		matplotlib.use("TkAgg")

	print(f"Calculate diffusion over {final_time} kyrs, hold tight.")

	elevation_after_diffusion = []
	slope_after_diffusion = []
	time_after_diffusion = []

	change_in_time = (0.1 * (change_in_distance ** 2)) / diffusion_coefficient

	distance = list(range(0, ((len(scarp_profile_elevation)) * change_in_distance), change_in_distance))
	elevation = scarp_profile_elevation

	slope = find_slope(elevation)
	slope_change = [0] * len(slope)

	plt.ion()

	if plot:
		fig = plt.figure()
		ax1 = fig.add_subplot(311)
		line1, = ax1.plot(distance, elevation, 'k-')
		line2, = ax1.plot(distance, elevation, 'r-')
		ax1.set_title('Height at time 0 kyr')
		plt.xlabel('distance along profile,m')
		plt.ylabel('elevation,m')

		ax2 = fig.add_subplot(312)
		line3, = ax2.plot(distance, slope, 'k-')
		line4, = ax2.plot(distance, slope, 'r-')
		ax2.set_title('Slope at time 0 kyr')
		plt.xlabel('distance along profile,m')
		plt.ylabel('Slope,m/m')

		ax3 = fig.add_subplot(313)
		line5, = ax3.plot(distance, slope_change, 'k-')
		line6, = ax3.plot(distance, slope_change, 'r-')
		ax3.set_title('Slope change at time 0 kyr');
		plt.xlabel('distance along profile,m');
		plt.ylabel('slope change (deg/m)');

	iteration = 1
	now_time = 0

	while now_time <= final_time:

		Q = (diffusion_coefficient * np.diff(elevation) / change_in_distance).tolist()
		Q.append(0)

		distance_elevation = ((np.diff(Q) / change_in_distance) * change_in_time).tolist()
		distance_elevation.insert(0, 0.0)
		distance_elevation.append(0.0)

		new_elevation = list(map(add, elevation, distance_elevation))
		slope = find_slope(new_elevation)

		slope_change = np.diff(slope).tolist()
		slope_change.append(0)
		slope_change = np.arctan(np.deg2rad(slope_change)).tolist()

		if plot == True and iteration / time_steps_between_plots == iteration // time_steps_between_plots:
			line2.set_xdata(distance)
			line2.set_ydata(new_elevation)
			ax1.set_title(f'Height at time {round(now_time, 1)} kyr')

			line4.set_xdata(distance)
			line4.set_ydata(slope)
			ax2.set_title(f'Slope at time {round(now_time, 1)} kyr')

			line6.set_xdata(distance)
			line6.set_ydata(slope_change)
			ax3.set_title(f'Slope change at time {round(now_time, 1)} kyr')

			fig.canvas.draw()
			fig.canvas.flush_events()

			time.sleep(0.01)

		now_time += change_in_time
		iteration += 1
		elevation = new_elevation

		elevation_after_diffusion.append(elevation)
		slope_after_diffusion.append(slope)
		time_after_diffusion.append(now_time)

	if plot:
		line2.set_xdata(distance)
		line2.set_ydata(new_elevation)
		line4.set_xdata(distance)
		line4.set_ydata(slope)
		line6.set_xdata(distance)
		line6.set_ydata(slope_change)

		fig.canvas.draw()
		plt.show()

	return (elevation_after_diffusion, slope_after_diffusion, time_after_diffusion)
