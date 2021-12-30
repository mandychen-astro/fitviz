from modelutils import get_muse_lsf, O3_1comp, O3_2comp, O3_3comp, O2_1comp
import numpy as np
from astropy.io import fits

def return_models():
    line = [3727.092, 3729.875]
    z0 = 0.5335
    line_z = np.asarray(line)*(1+z0)
    lsf = get_muse_lsf(line_z)
    func0 = O2_1comp(line, lsf).model_display

    line = [4960.295, 5008.240]
    z0 = 0.5335
    line_z = np.asarray(line)*(1+z0)
    lsf = get_muse_lsf(line_z)
    func1 = O3_1comp(line, lsf).model_display
    func2 = O3_2comp(line, lsf).model_display
    func3 = O3_3comp(line, lsf).model_display

    return func0, func1, func2

def return_bad_region_masks():
    mask1 = []
    mask2 = [7625, 7663]
    mask3 = [7625, 7663]
    return mask1, mask2, mask3
    # return []

def return_chi2_window():
    # return 
    return fits.getdata('/Users/mandychen/PKS0454-22/eso/mcmc_results/OIIIonly/dynamic_chi2_window.fits')




