import sys


def argschecker(args):
	if True not in list(vars(args).values()):
		print('ValueError: No arguments passed.')
		sys.exit()

	if args.filename is None and args.calculate_diffusion is True:
		print('ValueError: A input filename has not been passed.')
		sys.exit()

