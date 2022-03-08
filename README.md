# scarp-diffusion

[![Python application](https://github.com/mshodge/scarp-diffusion/actions/workflows/python-app.yml/badge.svg)](https://github.com/mshodge/scarp-diffusion/actions/workflows/python-app.yml)

Calculates the likely age of a fault scarp based from a diffusion cofficient. Generates the original fault surface and then diffuses the scarp and finds the best fit time.


## Get

1. To clone locally use:

    ```git clone https://github.com/mshodge/scarp-diffusion```

## Set

1. Install requirements to your chosen virtual environment:

    ```pip install -r requirements.txt```


2. Put your csv file with scarp profiles in `data` folder. The folder contains information about the schema needed.
 See `data/sample.csv` for example.

3. Update `config/config.py` with your chosen variables.


## Go

1. To run:

    ```
    python run_scarp_diffusion.py <args>
    ```

    Where `<args>` are:

        - `-filename`: the filename of your csv
        - `-synthetic`: if you want to process a synthetic scarp to see how the diffusion works
        - `-calculate_diffusion`: whther you want to calculate the diffusion for the file specified
        - `-use_smooth`: if you want to use a smoothed version of the scarp profile. Useful if the profile is noisy.
        - `s`: the smooth amount, default is 10

    This will save the outputs to the `/outputs/` folder.

## Additional Information

### Elevation Profiles

Profiles can be oriented as desired; typically they are oriented either perpendicular to the local scarp trend
(if slip direction is unknown), or perpendicular to the slip direction. Please note profiles length (in meters) and
distance between elevation measurement points, which should be equal to the DEM resolution.

## Acknowledgements

The code here is an adapted version of the [MATLAB code written by Ramon Arrowsmith](http://activetectonics.asu.edu/diffuse/).