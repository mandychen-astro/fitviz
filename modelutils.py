import os 
import numpy as np  
from scipy.interpolate import interp1d
from astropy.io import fits
from astropy.constants import c  


clight = c.value/1e3 # in unit of angstrom/s

def get_chi2_maps(config_params):
    paths = config_params.chi2_path
    if paths is None: return None
    fnames = config_params.chi2_fname
    all_chi2 = []
    for i in range(len(paths)):
        all_chi2.append(fits.getdata(paths[i]+fnames[i]))
    return all_chi2

def get_bic_maps(config_params):
    paths = config_params.bic_path
    if paths is None: return None
    fnames = config_params.bic_fname
    all_bic = []
    for i in range(len(paths)):
        all_bic.append(fits.getdata(paths[i]+fnames[i]))
    return all_bic

def get_model_popts(config_params):
    paths = config_params.model_path
    fnames = config_params.model_fname
    all_popts = []
    for i in range(len(paths)):
        all_popts.append(fits.getdata(paths[i]+fnames[i]))
    return all_popts

def get_muse_lsf(wave):
    l0, r0 = np.loadtxt(os.environ['HOME']+'/CUBS/muse_lsf.dat',unpack=True)
    r = interp1d(l0, r0)(wave)
    lsf = clight/r
    return lsf

def gauss(x, mu, sig, n):
    return n*np.exp(-(x-mu)**2/(2*sig**2))

def convolve_lsf(sig, lsf):
    a = 2*np.sqrt(2*np.log(2))
    return np.sqrt(sig**2+(lsf/a)**2)

class GaussSingleLine():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf  

    def model(self, x, z, sig, n):
        return gauss(x, self.lam0*(1. + z), 
            convolve_lsf(sig, self.lsf)/clight*self.lam0*(1. + z), n)

class O2_1comp():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf

    def model(self, x, z1, sig1, n1, ratio1):
        # note that n1 parameter is the amp. of blue component (3727A)
        n1_red = n1*ratio1
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1_red)
        return g1_blue + g1_red   

    def model_display(self, x, z1, sig1, n1, ratio1):
        n1_red = n1*ratio1
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1_red)
        return (g1_blue + g1_red, 
            g1_blue, g1_red)  

class O2_2comp():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf

    def model(self, x, z1, sig1, n1, ratio1, z2, sig2, n2, ratio2):
        # note that n1 parameter is the amp. of blue component (3727A)
        n1_red = n1*ratio1
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1_red)

        n2_red = n2*ratio2
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2_red)
        return g1_blue + g1_red + g2_blue + g2_red   

    def model_display(self, x, z1, sig1, n1, ratio1, z2, sig2, n2, ratio2):
        # note that n1 parameter is the amp. of blue component (3727A)
        n1_red = n1*ratio1
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1_red)

        n2_red = n2*ratio2
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2_red)
        return (g1_blue + g1_red + g2_blue + g2_red,
                g1_blue, g1_red, g2_blue, g2_red )  

class O3_1comp():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf

    def model(self, x, z1, sig1, n1):
        # note that n1 parameter is the amp. of red component (5008A)
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        return g1_blue + g1_red

    def model_nolsf(self, x, z1, sig1, n1):
        # note that n1 parameter is the amp. of red component (5008A)
        sig1_convolved = convolve_lsf(sig1, self.lsf[0])
        n1 = n1*sig1_convolved/sig1 # correct for narrowed line width without lsf
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            sig1/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            sig1/clight*self.lam0[1]*(1. + z1), 
            n1)
        return g1_blue + g1_red

    def model_display(self, x, z1, sig1, n1):
        return self.model(x, z1, sig1, n1)

    def model_nolsf_display(self, x, z1, sig1, n1):
        return self.model_nolsf(x, z1, sig1, n1)

class O3_2comp():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf

    def model(self, x, z1, sig1, n1, z2, sig2, n2):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        return g1_blue + g1_red + g2_blue + g2_red

    def model_nolsf(self, x, z1, sig1, n1, z2, sig2, n2):
        sig1_convolved = convolve_lsf(sig1, self.lsf[0])
        n1 = n1*sig1_convolved/sig1 # correct for narrowed line width without lsf
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            sig1/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            sig1/clight*self.lam0[1]*(1. + z1), 
            n1)
        sig2_convolved = convolve_lsf(sig2, self.lsf[0])
        n2 = n2*sig2_convolved/sig2 # correct for narrowed line width without lsf
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            sig2/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            sig2/clight*self.lam0[1]*(1. + z2), 
            n2)
        return g1_blue + g1_red + g2_blue + g2_red

    def model_display(self, x, z1, sig1, n1, z2, sig2, n2):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        return (g1_blue + g1_red + g2_blue + g2_red, 
                g1_blue + g1_red, g2_blue + g2_red) 

    def model_nolsf_display(self, x, z1, sig1, n1, z2, sig2, n2):
        sig1_convolved = convolve_lsf(sig1, self.lsf[0])
        n1 = n1*sig1_convolved/sig1 # correct for narrowed line width without lsf
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            sig1/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            sig1/clight*self.lam0[1]*(1. + z1), 
            n1)
        sig2_convolved = convolve_lsf(sig2, self.lsf[0])
        n2 = n2*sig2_convolved/sig2 # correct for narrowed line width without lsf
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            sig2/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            sig2/clight*self.lam0[1]*(1. + z2), 
            n2)
        return (g1_blue + g1_red + g2_blue + g2_red,
                g1_blue + g1_red, g2_blue + g2_red)

class O3_3comp():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf

    def model(self, x, z1, sig1, n1, z2, sig2, n2, z3, sig3, n3):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        n3_blue = n3/3.
        g3_blue = gauss(x, self.lam0[0]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[0])/clight*self.lam0[0]*(1. + z3),
            n3_blue)
        g3_red = gauss(x, self.lam0[1]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[1])/clight*self.lam0[1]*(1. + z3), 
            n3)
        return g1_blue + g1_red + g2_blue + g2_red + g3_blue + g3_red

    def model_display(self, x, z1, sig1, n1, z2, sig2, n2, z3, sig3, n3):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        n3_blue = n3/3.
        g3_blue = gauss(x, self.lam0[0]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[0])/clight*self.lam0[0]*(1. + z3),
            n3_blue)
        g3_red = gauss(x, self.lam0[1]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[1])/clight*self.lam0[1]*(1. + z3), 
            n3)
        return (g1_blue + g1_red + g2_blue + g2_red + g3_blue + g3_red,
                g1_blue + g1_red, g2_blue + g2_red, g3_blue + g3_red)

class O3_4comp():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf

    def model(self, x, z1, sig1, n1, z2, sig2, n2, z3, sig3, n3, z4, sig4, n4):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        n3_blue = n3/3.
        g3_blue = gauss(x, self.lam0[0]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[0])/clight*self.lam0[0]*(1. + z3),
            n3_blue)
        g3_red = gauss(x, self.lam0[1]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[1])/clight*self.lam0[1]*(1. + z3), 
            n3)
        n4_blue = n4/3.
        g4_blue = gauss(x, self.lam0[0]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[0])/clight*self.lam0[0]*(1. + z4),
            n4_blue)
        g4_red = gauss(x, self.lam0[1]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[1])/clight*self.lam0[1]*(1. + z4), 
            n4)
        return g1_blue + g1_red + g2_blue + g2_red + g3_blue + g3_red + g4_blue + g4_red

    def model_display(self, x, z1, sig1, n1, z2, sig2, n2, z3, sig3, n3, z4, sig4, n4):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        n3_blue = n3/3.
        g3_blue = gauss(x, self.lam0[0]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[0])/clight*self.lam0[0]*(1. + z3),
            n3_blue)
        g3_red = gauss(x, self.lam0[1]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[1])/clight*self.lam0[1]*(1. + z3), 
            n3)
        n4_blue = n4/3.
        g4_blue = gauss(x, self.lam0[0]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[0])/clight*self.lam0[0]*(1. + z4),
            n4_blue)
        g4_red = gauss(x, self.lam0[1]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[1])/clight*self.lam0[1]*(1. + z4), 
            n4)
        return (g1_blue + g1_red + g2_blue + g2_red + g3_blue + g3_red + g4_blue + g4_red,
            g1_blue + g1_red, g2_blue + g2_red, g3_blue + g3_red, g4_blue + g4_red)

class O3_5comp():
    def __init__(self, lam0, lsf):
        self.lam0 = lam0
        self.lsf = lsf

    def model(self, x, z1, sig1, n1, z2, sig2, n2, z3, sig3, n3, z4, sig4, n4, z5, sig5, n5):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        n3_blue = n3/3.
        g3_blue = gauss(x, self.lam0[0]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[0])/clight*self.lam0[0]*(1. + z3),
            n3_blue)
        g3_red = gauss(x, self.lam0[1]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[1])/clight*self.lam0[1]*(1. + z3), 
            n3)
        n4_blue = n4/3.
        g4_blue = gauss(x, self.lam0[0]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[0])/clight*self.lam0[0]*(1. + z4),
            n4_blue)
        g4_red = gauss(x, self.lam0[1]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[1])/clight*self.lam0[1]*(1. + z4), 
            n4)
        n5_blue = n5/3.
        g5_blue = gauss(x, self.lam0[0]*(1. + z5), 
            convolve_lsf(sig5, self.lsf[0])/clight*self.lam0[0]*(1. + z5),
            n5_blue)
        g5_red = gauss(x, self.lam0[1]*(1. + z5), 
            convolve_lsf(sig5, self.lsf[1])/clight*self.lam0[1]*(1. + z5), 
            n5)
        return g1_blue + g1_red + g2_blue + g2_red + g3_blue + g3_red + g4_blue + g4_red + g5_blue + g5_red

    def model_display(self, x, z1, sig1, n1, z2, sig2, n2, z3, sig3, n3, z4, sig4, n4, z5, sig5, n5):
        n1_blue = n1/3.
        g1_blue = gauss(x, self.lam0[0]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[0])/clight*self.lam0[0]*(1. + z1),
            n1_blue)
        g1_red = gauss(x, self.lam0[1]*(1. + z1), 
            convolve_lsf(sig1, self.lsf[1])/clight*self.lam0[1]*(1. + z1), 
            n1)
        n2_blue = n2/3.
        g2_blue = gauss(x, self.lam0[0]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[0])/clight*self.lam0[0]*(1. + z2),
            n2_blue)
        g2_red = gauss(x, self.lam0[1]*(1. + z2), 
            convolve_lsf(sig2, self.lsf[1])/clight*self.lam0[1]*(1. + z2), 
            n2)
        n3_blue = n3/3.
        g3_blue = gauss(x, self.lam0[0]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[0])/clight*self.lam0[0]*(1. + z3),
            n3_blue)
        g3_red = gauss(x, self.lam0[1]*(1. + z3), 
            convolve_lsf(sig3, self.lsf[1])/clight*self.lam0[1]*(1. + z3), 
            n3)
        n4_blue = n4/3.
        g4_blue = gauss(x, self.lam0[0]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[0])/clight*self.lam0[0]*(1. + z4),
            n4_blue)
        g4_red = gauss(x, self.lam0[1]*(1. + z4), 
            convolve_lsf(sig4, self.lsf[1])/clight*self.lam0[1]*(1. + z4), 
            n4)
        n5_blue = n5/3.
        g5_blue = gauss(x, self.lam0[0]*(1. + z5), 
            convolve_lsf(sig5, self.lsf[0])/clight*self.lam0[0]*(1. + z5),
            n5_blue)
        g5_red = gauss(x, self.lam0[1]*(1. + z5), 
            convolve_lsf(sig5, self.lsf[1])/clight*self.lam0[1]*(1. + z5), 
            n5)
        return (g1_blue + g1_red + g2_blue + g2_red + g3_blue + g3_red + g4_blue + g4_red + g5_blue + g5_red,
            g1_blue + g1_red, g2_blue + g2_red, g3_blue + g3_red, g4_blue + g4_red, g5_blue + g5_red)