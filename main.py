import sys
import shutil
from fitviz.config import DefineParams
from fitviz.displayutils import Displays
from fitviz.datautils import Data
from fitviz.modelutils import get_model_popts, get_chi2_maps, get_bic_maps

def main():
	# parse configuration
	config_fname = sys.argv[1]
	model_config_fname = sys.argv[2]
	shutil.copy(model_config_fname, './model_config.py')
	config_params = DefineParams(config_fname)

	# read in data
	data = Data(config_params)

	# read in model parameters
	model_popts = get_model_popts(config_params)
	chi2_maps = get_chi2_maps(config_params)
	bic_maps = get_bic_maps(config_params)

	# set up windows
	displays = Displays(config_params, data, model_popts, chi2_maps, bic_maps)
	displays.set_full_window()
	displays.run()

main()
	
