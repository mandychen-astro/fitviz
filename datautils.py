from astropy.io import fits
import numpy as np 


# need: init_map, cube, wave
class Data():
    def __init__(self, config_params):
        self.config_params = config_params

        map_fullpath = config_params.map_path + config_params.map_fname
        self.init_map = fits.getdata(map_fullpath)

        # read cube data and close it after getting the values
        cube_fullpath = config_params.cube_path + config_params.cube_fname
        hdul = fits.open(cube_fullpath)
        if len(hdul) < 3: warnings.warn('datacube missing variance extension')

        self.datacube = hdul[1].data
        self.varcube = hdul[2].data

        h = hdul[1].header
        self.wave = h['CRVAL3'] + h['CD3_3']*np.arange(h['NAXIS3'])

        hdul.close()


