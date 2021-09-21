import sys
from fitviz.config import DefineParams
from fitviz.displayutils import Displays
from fitviz.datautils import Data
from fitviz.modelutils import get_model_popts

def main():
	# parse configuration
	config_fname = sys.argv[1]
	config_params = DefineParams(config_fname)

	# read in data
	data = Data(config_params)

	# read in model parameters
	model_popts = get_model_popts(config_params)

	# set up windows
	displays = Displays(config_params, data, model_popts)
	displays.set_full_window()
	displays.run()

main()
	
