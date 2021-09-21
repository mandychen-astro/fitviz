from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from astropy.visualization import ZScaleInterval
from astropy.io import fits
import numpy as np 

from fitviz.model_config import return_models


rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)

def nice_axis(ax, tick_label_size=12, tick_length=6, tick_minor_length=3):
    ax.tick_params(which='major',labelsize=tick_label_size)
    ax.tick_params(direction="in",length=tick_length)
    ax.minorticks_on()
    ax.tick_params(which="minor",direction="in",length=tick_minor_length)
    ax.tick_params(axis='y',which='both',right=True)
    ax.tick_params(axis='x',which='both',top=True)

class Cursor:
    def __init__(self, ax, canvas, data):
        self.ax = ax
        self.canvas = canvas
        self.data = data

        # text location in axes coords
        self.txt = self.ax.text(0.7, 1.03, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the cursor positions
        self.txt.set_text('x=%d, y=%d, value=%.2f' % (x, y, self.data[int(y), int(x)]))
        self.canvas.draw()

class Displays():
    def __init__(self, config_params, data, model_popts):
        self.config_params = config_params
        self.data = data
        self.datacube = data.datacube
        self.errcube = np.sqrt(data.varcube)*config_params.rescale_noise
        self.wave = data.wave
        self.models = return_models()
        self.model_popts = model_popts
        self.linestyles = ['solid', 'dashed', 'dashed', 'dashed', 'dashed', 'dashed']
        self.colors = ['tab:red', 'tab:green', 'tab:orange', 'tab:blue', 'tab:purple', 'tab:brown']

    def set_full_window(self):
        self.root = Tk()

        self.frame1 = Frame(self.root)
        # self.frame2 = LabelFrame(self.root, text='Test', font=('calibre',12,'normal'),
        #                         labelanchor='n')
        self.frame2 = Frame(self.root)

        self.frame1.pack(side = LEFT, fill = BOTH, expand = True) 
        self.frame2.pack(side = LEFT, fill = BOTH, expand = True) 

        self.frame1.rowconfigure(0, weight=8)
        self.frame1.rowconfigure(1, weight=1)
        self.frame1.rowconfigure(2, weight=3)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.columnconfigure(2, weight=1)
        self.frame1.columnconfigure(3, weight=1)


        ###### FOR TESTING, DELETE LATER #########  
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.rowconfigure(1, weight=1)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.frame2.columnconfigure(2, weight=1)
        self.frame2.columnconfigure(3, weight=1)
        ###### FOR TESTING, DELETE LATER #########  


        # display the full 2d image
        self.show_2d_image()

        # display the buttons
        self.show_resize_buttons()

        # display the full spec
        self.show_full_spec()

        # display zoom in windows
        self.show_zoomin_spec()

        # display models in windows
        self.show_models()

    def zoom_2Dwindow(self, coord_var):
        coords = coord_var.get()
        coords = [int(i) for i in coords.split(',')]
        self.ax1.set_xlim(coords[0], coords[1])
        self.ax1.set_ylim(coords[2], coords[3])
        # self.ax1.get_xaxis().set_visible(False)
        # self.ax1.axes.get_yaxis().set_visible(False)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0, columnspan=4, sticky = NSEW)

    def onclick_cube(self, event):
        ynew, xnew = int(event.ydata), int(event.xdata)

        self.lx.set_ydata(ynew)
        self.ly.set_xdata(xnew)
        self.ax1.set_title('x={}, y={}'.format(xnew, ynew), fontsize=12)

        self.ax2.clear()
        mask = (self.wave>self.wmin0) & (self.wave<self.wmax0)
        self.ax2.step(self.wave[mask], self.datacube[:, ynew, xnew][mask], 
                            where='mid',color='k', linewidth=0.5)
        self.ax2.hlines(0, self.wave[mask][0], self.wave[mask][-1], linestyle='dashed', color='gray')
        self.ax2.set_xlabel(r'Observed wavelength ($\mathrm{\AA}$)', fontsize=12)
        self.ax2.set_ylabel(r'$F_\lambda$', fontsize=12)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=2, columnspan=4, sticky = NSEW)

        spec_pix = self.datacube[:, ynew, xnew]
        specerr_pix = self.errcube[:, ynew, xnew]

        for ipanel in range(self.npanels):
            mask = (self.wave > self.wmins[ipanel]) & (self.wave < self.wmaxs[ipanel])
            model = self.models[ipanel](self.xmodels[ipanel], 
                                        *self.model_popts[ipanel][:, ynew, xnew])
            self.axes[ipanel].clear()
            self.axes[ipanel].step(self.wave[mask], spec_pix[mask], where='mid', color='k')
            self.axes[ipanel].step(self.wave[mask], specerr_pix[mask], where='mid', color='b')
            nmodels = len(model)
            try:
                for i in range(nmodels):
                    self.axes[ipanel].plot(self.xmodels[ipanel], model[i], 
                                           linestyle=self.linestyles[i], 
                                           c=self.colors[i])
            except: self.axes[ipanel].plot(self.xmodels[ipanel], model, 
                                           linestyle=self.linestyles[0], 
                                           c=self.colors[0])
            self.axes[ipanel].set_ylabel(r'$F_\lambda$', fontsize=12)
        self.axes[-1].set_xlabel(r'Observed wavelength ($\mathrm{\AA}$)', fontsize=12)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().pack(fill = BOTH, expand = True, padx = 10, pady=2)

    def show_2d_image(self):
        init_map = self.data.init_map
        vmin, vmax = self.config_params.vmin, self.config_params.vmax
        color_bar_label = self.config_params.color_bar_label

        self.y0 = int(init_map.shape[0]/2)
        self.x0 = int(init_map.shape[1]/2)

        self.fig1 = plt.figure(figsize=(5,5))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_title('x={}, y={}'.format(self.x0, self.y0), fontsize=12)
        self.im1 = self.ax1.imshow(init_map, cmap = 'jet', vmin = vmin, 
                                    vmax = vmax, origin='lower')
        divider = make_axes_locatable(self.ax1)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = self.fig1.colorbar(self.im1, cax=cax)
        cb.set_label(color_bar_label,fontsize=12)

        # draw dashed cross to show where the pointed pixel is
        self.lx = self.ax1.axhline(color='k', linestyle='dashed')
        self.ly = self.ax1.axvline(color='k', linestyle='dashed')
        self.lx.set_ydata(self.y0)
        self.ly.set_xdata(self.x0)

        # put it into the frame
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.frame1)  
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0, columnspan=4, sticky = NSEW)

        # set up interative functions
        self.canvas1.mpl_connect('button_press_event', self.onclick_cube)
        self.cursor = Cursor(self.ax1, self.canvas1, init_map)
        self.canvas1.mpl_connect('motion_notify_event', self.cursor.mouse_move)

    def show_resize_buttons(self):
        # find area to display
        xmin, xmax = self.config_params.xmin, self.config_params.xmax
        ymin, ymax = self.config_params.ymin, self.config_params.ymax

        coord_var=StringVar()
        coord_label = Label(self.frame1, text='Zoom to xmin, xmax, ymin, ymax: ',
                            font=('calibre',12,'normal'))
        coord_entry = Entry(self.frame1, textvariable = coord_var)
        coord_entry.insert(10, '{},{},{},{}'.format(xmin, xmax, ymin, ymax))
        coord_label.grid(row=1, column=0, padx = 5, pady=2, sticky = NSEW)
        coord_entry.grid(row=1, column=1, sticky = NSEW)

        zoom_button = Button(self.frame1, text='Zoom', font=('calibre',12,'normal'), 
                            command=lambda: self.zoom_2Dwindow(coord_var))
        zoom_button.grid(row=1, column=2, sticky=NSEW)

        fullframe_button = Button(self.frame1, text='Back to full frame', 
                                    font=('calibre',12,'normal'))
        fullframe_button.grid(row=1, column=3, sticky=NSEW)

    def show_full_spec(self):
        init_spec = self.datacube[:, self.y0, self.x0]
        self.wmin0, self.wmax0 = self.config_params.wmin0, self.config_params.wmax0
        self.fig2 = plt.figure(figsize=(6,2))
        self.ax2 = self.fig2.add_subplot(111)
        mask = (self.wave>self.wmin0) & (self.wave<self.wmax0)
        self.ax2.step(self.wave[mask], init_spec[mask], where='mid',color='k', linewidth=0.5)
        self.ax2.set_xlabel(r'Observed wavelength ($\mathrm{\AA}$)', fontsize=12)
        self.ax2.set_ylabel(r'$F_\lambda$', fontsize=12)
        self.ax2.hlines(0, self.wave[mask][0], self.wave[mask][-1], linestyle='dashed', color='gray')
        nice_axis(self.ax2)
        self.fig2.tight_layout()
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.frame1)  # A tk.DrawingArea.
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=2, columnspan=4, sticky = NSEW)

    def show_zoomin_spec(self):
        self.npanels = self.config_params.npanels
        self.wmins, self.wmaxs = self.config_params.wmins, self.config_params.wmaxs
        spec_pix = self.datacube[:, self.y0, self.x0]
        specerr_pix = self.errcube[:, self.y0, self.x0]

        self.fig3, self.axes = plt.subplots(self.npanels, 1, figsize=(4,2*self.npanels))
        for ipanel in range(self.npanels):
            mask = (self.wave > self.wmins[ipanel]) & (self.wave < self.wmaxs[ipanel])
            self.axes[ipanel].step(self.wave[mask], spec_pix[mask], where='mid', color='k')
            self.axes[ipanel].step(self.wave[mask], specerr_pix[mask], where='mid', color='b')
            self.axes[ipanel].set_ylabel(r'$F_\lambda$', fontsize=12)
            nice_axis(self.axes[ipanel])
        self.axes[-1].set_xlabel(r'Observed wavelength ($\mathrm{\AA}$)', fontsize=12)
        self.fig3.tight_layout()
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.frame2)  
        self.canvas3.draw()
        self.canvas3.get_tk_widget().pack(fill = BOTH, expand = True, padx = 10, pady=2)

    def _get_xmodel_range(self):
        self.xmodels = []
        for ipanel in range(self.npanels):
            self.xmodels.append(np.arange(self.wmins[ipanel], self.wmaxs[ipanel], 0.1))

    def show_models(self):
        self._get_xmodel_range()
        for ipanel in range(self.npanels):
            model = self.models[ipanel](self.xmodels[ipanel], 
                                        *self.model_popts[ipanel][:,self.y0, self.x0])
            nmodels = len(model)
            try:
                for i in range(nmodels):
                    self.axes[ipanel].plot(self.xmodels[ipanel], model[i], 
                                           linestyle=self.linestyles[i], 
                                           c=self.colors[i])
            except: self.axes[ipanel].plot(self.xmodels[ipanel], model, 
                                           linestyle=self.linestyles[0], 
                                           c=self.colors[0])

    def run(self):
        self.root.mainloop()













