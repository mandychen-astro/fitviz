import numpy as np 
import re

class DefineParams():
    def __init__(self, config_fname):
        self.config_fname = config_fname

        # Read and filter empty lines
        all_lines = filter(None,(line.rstrip() for line in open(config_fname)))

        # Remove commented lines
        self.lines = []
        for line in all_lines:
            if not line.startswith('#'): 
                self.lines.append(line)

        for line_str in self.lines:
            line = list(filter(None,line_str.split(' ')))
            if 'map_path' in line:
                self.map_path = line[1]
            if 'map_fname' in line:
                self.map_fname = line[1]
            if 'cube_path' in line:
                self.cube_path = line[1]
            if 'cube_fname' in line:
                self.cube_fname = line[1]
            if 'model_path' in line:
                self.model_path = [x for x in line[1:]]
            if 'model_fname' in line:
                self.model_fname = [x for x in line[1:]]
            if 'chi2_path' in line:
                self.chi2_path = [x for x in line[1:]]
            if 'chi2_fname' in line:
                self.chi2_fname = [x for x in line[1:]]
            if 'bic_path' in line:
                self.bic_path = [x for x in line[1:]]
            if 'bic_fname' in line:
                self.bic_fname = [x for x in line[1:]]
            if 'vmin' in line:
                self.vmin, self.vmax = int(line[2]), int(line[3])
            if 'xmin' in line:
                self.xmin, self.xmax = int(line[2]), int(line[3])
            if 'ymin' in line:
                self.ymin, self.ymax = int(line[2]), int(line[3])
            if 'wmin' in line:
                self.wmin, self.wmax = int(line[2]), int(line[3])
            if 'color_bar_label' in line:
                total_len = len(line)
                label = ''
                for i in range(1, total_len): label += (line[i]+' ')
                self.color_bar_label = label[1:-2]
            if 'npanels' in line:
                self.npanels = int(line[1])
            if 'wmins' in line:
                self.wmins = [int(x) for x in line[1:]]
            if 'wmaxs' in line:
                self.wmaxs = [int(x) for x in line[1:]]
            if 'rescale_noise' in line:
                self.rescale_noise = float(line[1])
            if 'panel_titles' in line:
                self.panel_titles = re.findall('\'([^\']*)\'', line_str)

        if not hasattr(self, 'map_path'):
            self.map_path = self.cube_path
        if not hasattr(self, 'chi2_path'):
            self.chi2_path = None
        if not hasattr(self, 'bic_path'):
            self.bic_path = None
            
