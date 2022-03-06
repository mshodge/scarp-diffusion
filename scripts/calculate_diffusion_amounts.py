import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.metrics import mean_squared_error

from config import config
from scripts.utils.fit_poly import fit_poly
from scripts.utils.diffuse import diffuse


def save_to_csv(df):
    """
    Saves DataFrame to csv file.
    :param df <pandas.DataFrame> A pandas DataFrame to save
    :return: pandas.DataFrame.to_csv
    """

    filename = f'diffusion_calculation.csv'
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', filename)
    return df.to_csv(save_path, index=False)


def tellme(s):
    """
    Prints a string to a plot
    :param s: <string> The title to be printed
    """

    plt.title(s, fontsize=16)
    plt.draw()


def create_dataframe_to_save(df, best_fit_and_rmse):
    """
    Saves the results as a DataFrame
    :param df: <pandas.DataFrame> The dataframe with profile distance and elevation
    :param best_fit_and_rmse: <tuple> The best fit and its rmse
    :return df_to_save: <pandas.DataFrame> The dataframe to save
    """

    df_to_save = pd.DataFrame(
        {"profile": list(set(df['profile'])),
         "age": best_fit_and_rmse[0],
         "rmse": best_fit_and_rmse[1]})

    return df_to_save


def plot_profiles_get_crest_and_base(df, use_smooth):
    """
    Plot profiles and ask user to select crest and base
    :param df: <pandas.DataFrame> The dataframe with profile distance and elevation
    :return base, crest: <tuple> The distance and height of the base and crest on the profile
    """

    plt.figure(1)
    plt.plot(df["dist"], df["elevation"])
    if use_smooth:
        plt.plot(df["dist"], df["elevation_raw"])
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')
    tellme('Select the scrap crest, then scarp base. Click to begin.')

    pts = plt.ginput(3, timeout=0)  # it will wait for three clicks
    pts = np.array(pts)
    if len(pts) == 3:
        plt.close()

    # Saves the user specified location of the crest and the base
    base = [pts[1, 0], pts[1, 1]]
    crest = [pts[0, 0], pts[0, 1]]

    return (base, crest)


def calculate_rmse(df, height):
    """
    Calculate the root mean square error between the calculated elevation and dataframe
    :param df: <pandas.DataFrame> The dataframe with profile distance and elevation
    :return height: <list> The elevation values from the diffuse calculation
    :return rmse_list: <list> The rmse list
    """

    rmse_list = []

    for n in range(0, len(df)):
        rmse_list.append(mean_squared_error(df['elevation'], height[n], squared=False))

    return rmse_list


def find_best_fit(df, diffusion_coefficient, calculation_final_time, time_steps_between_plots, use_smooth, smooth_amount,
                  plot=False):
    """
    Find the best fit between the original profile and the diffuse profiles
    :param df: <pandas.DataFrame> The dataframe with profile distance and height
    :param diffusion_coefficient: <int> The diffusion coefficient in mm per year
    :param calculation_final_time: <int> The final time in kyr
    :param time_steps_between_plots: <int> the time step between plots
    :param plot: <boolean> Whether  to plot the diffusion profiles or not
    :return best_diff, best_rmse: <tuple> The best diffusion amount and its rmse
    """

    profiles = list(set(df['profile'].to_list()))

    best_diffusion_amount = []
    best_rmse = []

    for profile in profiles:

        profile_df = df[df["profile"] == profile].reset_index()

        if use_smooth:
            # Make new column for raw data and make the smoothed data the one used for the diffusion calculations
            profile_df['elevation_raw'] = profile_df['elevation']
            profile_df['elevation'] = profile_df['elevation_raw'].rolling(smooth_amount, min_periods=1).mean()

        base_and_crest = plot_profiles_get_crest_and_base(profile_df, use_smooth)

        profile_df_simple = profile_df.copy()

        rmse_upper, upper, upper_poly_height, p_upper = fit_poly(profile_df, base_and_crest[0][0], base_and_crest[1][0],
                                                                 where="upper")
        rmse_lower, lower, lower_poly_height, p_lower = fit_poly(profile_df, base_and_crest[0][0], base_and_crest[1][0],
                                                                 where="lower")

        profile_dist_crest = profile_df['dist'].values[int(base_and_crest[1][0])]
        profile_dist_base = profile_df['dist'].values[int(base_and_crest[0][0])]
        scarp_height = upper_poly_height[profile_dist_crest] - lower_poly_height[profile_dist_base]
        scarp_height_per_distance = scarp_height / (profile_dist_base - profile_dist_crest + 1)

        new_elevation = [0] * len(profile_df)

        num = 1
        for index, row in profile_df_simple.iterrows():
            if row['dist'] < profile_dist_crest:
                new_elevation[index] = upper_poly_height[index]
            if profile_dist_crest <= row['dist'] <= profile_dist_base:
                new_elevation[index] = upper_poly_height[profile_dist_crest] - (scarp_height_per_distance * num)
                num += 1
            if row['dist'] > profile_dist_base:
                new_elevation[index] = lower_poly_height[index]

        profile_df_simple['elevation'] = new_elevation

        change_in_distance = profile_df_simple['dist'].values[1] - profile_df_simple['dist'].values[0]

        diffusion_values = diffuse(change_in_distance, new_elevation, diffusion_coefficient, calculation_final_time,
                                   time_steps_between_plots, plot=False);

        diffusion_amount = diffusion_values[2] * diffusion_coefficient

        rmse_list = calculate_rmse(profile_df, diffusion_values[0])

        best_diffusion_amount.append(diffusion_amount[rmse_list.index(min(rmse_list))])

        best_rmse.append(min(rmse_list))

    return (best_diffusion_amount, best_rmse)


def calculate_diffusion_amounts(df, use_smooth, smooth_amount, config):
    """
    Runs pipeline and saves output
    :param df: <pandas.DataFrame> The dataframe with profile distance and elevation
    """

    best_fit_and_rmse = find_best_fit(df, config.diffusion_coefficient, config.calculation_final_time,
                                      config.time_steps_between_plots, use_smooth, smooth_amount,
                                      plot=False)
    df_to_save = create_dataframe_to_save(df, best_fit_and_rmse)
    save_to_csv(df_to_save)


if __name__ == "__main__":
    df = pd.read_csv('../data/Profiles2.csv').reset_index()
    use_smooth = True
    smooth_amount = 10
    calculate_diffusion_amounts(df, use_smooth, smooth_amount, config)
