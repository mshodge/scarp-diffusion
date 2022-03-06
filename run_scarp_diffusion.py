import argparse
import pandas as pd

from scripts.build_synthetic_scarp_and_diffuse import build_synthetic_scarp_and_diffuse
from scripts.calculate_diffusion_amounts import calculate_diffusion_amounts
from scripts.utils.argschecker import argschecker
from config import config


def main(filename, synthetic, calculate_diffusion, use_smooth, smooth_amount, config):

    if synthetic:
        build_synthetic_scarp_and_diffuse(config)

    if calculate_diffusion:
        df = pd.read_csv(f'./data/{filename}').reset_index()
        calculate_diffusion_amounts(df, use_smooth, smooth_amount, config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-filename', default=None,
                        help='The filename of the profiles to analyse.')
    parser.add_argument('-synthetic', action='store_true', default=False,
                        help='Create synthetic profiles to see how the diffusion works.')
    parser.add_argument('-calculate_diffusion', action='store_true', default=False,
                        help='Calculate diffusion amounts based on best fits.')
    parser.add_argument('-use_smooth', action='store_true', default=False,
                        help='Use a smoothed profile instead of the original points if the profile is noisy.')
    parser.add_argument('-s', default=10,
                        help='The smooth amount to use (default is 10).')
    args = parser.parse_args()

    argschecker(args)

    main(filename=args.filename, synthetic=args.synthetic, calculate_diffusion=args.calculate_diffusion,
         use_smooth=args.use_smooth, smooth_amount=args.s, config=config)
