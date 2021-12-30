from modelutils import get_muse_lsf, O2_1comp, O3_1comp
import numpy as np

def return_models():
	line = [3727.092, 3729.875]
	z0 = 0.7861
	line_z = np.asarray(line)*(1+z0)
	lsf = get_muse_lsf(line_z)
	o2_1comp = O2_1comp(line, lsf)
	func1 = o2_1comp.model_display

	line = [4960.295, 5008.240]
	z0 = 0.7861
	line_z = np.asarray(line)*(1+z0)
	lsf = get_muse_lsf(line_z)
	o3_1comp = O3_1comp(line, lsf)
	func2 = o3_1comp.model_display
	return func1, func2


