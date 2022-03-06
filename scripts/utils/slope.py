def find_slope(elevation):
    """
    Performs the diffusion calculation on a scarp profile
    :param elevation: <list> The elevation of the scarp profile
    :return slope: <list> The calculated slope
    """

    slope = []

    for n in list(range(0, len(elevation))):
        if n > 1:
            slope.append(elevation[n] - elevation[n-1]);
        else:
            slope.append(0)
    return slope
