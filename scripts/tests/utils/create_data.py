import pandas as pd


def create_diffused_profile():
    df = pd.DataFrame({"elevation_smooth": [8.7, 8.7, 8.7, 8.6, 8.6, 8.6, 8.6, 8.5, 8.4, 8.2,
                                            8.0, 7.6, 7.2, 6.7, 6.1, 5.4, 4.7, 4.0, 3.2, 2.6,
                                            2.0, 1.4, 1.0, 0.7, 0.5, 0.3, 0.2, 0.1, 0.1, 0.0],
                       "dist": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
                       })
    return df