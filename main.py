# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtWidgets, QtGui

#plotting
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

#other imports
import sys
import math
import numpy as np

import custom_widgets
import layer_builder

"""
NOTES:

All angles in radians, unless otherwised specified

"""


#convert energy in eVs to wavenumber in A^-1
def evtok(energy_evs):
    return 0.5123*math.sqrt(energy_evs)

#quadratic solve for sz
def delta_sz(sx,sy, theta_i, phi_i, k):
    a = 1
    b = -2*k*np.sin(theta_i) #must be in radians
    c = pow(sx,2) + pow(sy,2) +2*k*np.cos(theta_i)*(sx*np.cos(phi_i)+sy*np.sin(phi_i))
    roots = np.roots([a,b,c])
    return np.array(roots)[~np.iscomplex(roots)]

#solve for theta and phi final values
def thetaphi_sets(dim, a_recip, b_recip, gamma, theta_i, phi_i, k):
    thetaphisets = np.full((pow(dim,2),3),-1.)
    degreesphi = int(np.degrees(phi_i)*0.25)
    indx = 0
    for x in range(-(int (dim/2)), int((dim+1)/2)): #start from farthest point go back toward specular
        for y in range(-(int (dim/2)), int((dim+1)/2)): #start from one side sweep to other, origin at middle
            sy = x*a_recip + y*b_recip*np.cos(np.radians(gamma))
            sx = y*b_recip*np.sin(np.radians(gamma))
            sz = delta_sz(sx, sy, theta_i, phi_i, k)
            if sz.size == 0:
                pass
            else:
                theta_f = np.arcsin(np.max(sz) / k - np.sin(theta_i))
                phi_f = np.arctan2(sy/k+np.cos(theta_i)*np.sin(phi_i), sx/k+np.cos(theta_i)*np.cos(phi_i)) - phi_i
                thetaphisets[indx] = np.array([theta_f,phi_f,1]) #last digit placeholder for intensity
                indx += 1

    return thetaphisets

#main window
class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(QtCore.QRect(30, 30, 1200, 1000))
        self.setWindowTitle("RHEED Simulator")

        #create figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        #layer builder
        self.add_layer_button = QtWidgets.QPushButton("Add Layer")
        self.edit_layer_button = QtWidgets.QPushButton("Edit Layer")
        self.remove_layer_button = QtWidgets.QPushButton("Remove Layer")
        self.add_layer_button.clicked.connect(self.new_layer)
        self.edit_layer_button.clicked.connect(self.edit_layer)
        self.remove_layer_button.clicked.connect(self.remove_layer)
        self.layers = custom_widgets.DragWidget(orientation=QtCore.Qt.Orientation.Vertical)

        #labels
        params_label = QtWidgets.QLabel("RHEED Parameters")
        layers_label = QtWidgets.QLabel("Material Layers")
        top_layer_label = QtWidgets.QLabel("Top Layer")
        bottom_layer_label = QtWidgets.QLabel("Bottom Layer")

        #slider/values
        #theta and phi are multiplied by 100
        degrees = '\u00b0'
        theta = chr(0x03B8)
        self.theta_i = custom_widgets.CustomDoubleSlider(0,5,3.8, "incident angle (%s)" %(degrees)) #degrees
        self.phi_i = custom_widgets.CustomDoubleSlider(0,45,0, "azimuthal angle (%s)" %(degrees))
        self.energy = custom_widgets.CustomDoubleSlider(10,30,10.5, "energy (keV)") #electron-volts
        self.screen_distance = custom_widgets.CustomDoubleSlider(20,60,50, "screen distance (cm)")
        

        #button
        #self.plot()
        self.plotbutton = QtWidgets.QPushButton('Plot')
        #self.plotbutton.clicked.connect(lambda: self.load_cif())
        self.plotbutton.clicked.connect(self.plot)
        
        
        #add widgets to window
        layout = QtWidgets.QVBoxLayout()

        #header of layout // lo stands for layout
        #lo_header = QtWidgets.QHBoxLayout()
        #lo_header.addWidget(self.browser)

        #body of layout
        lo_body = QtWidgets.QHBoxLayout()

        #left side of body
        lo_bodyleft = QtWidgets.QVBoxLayout()
        lo_bodyleft.addWidget(self.toolbar)
        lo_bodyleft.addWidget(self.canvas)

        #right side of body
        lo_bodyright = QtWidgets.QVBoxLayout()
        verticalSpacer = QtWidgets.QSpacerItem(2, 0, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Expanding)

        #layers row
        lo_layers_row = QtWidgets.QHBoxLayout()
        lo_layers_row.addWidget(self.add_layer_button)
        lo_layers_row.addWidget(self.edit_layer_button)
        lo_layers_row.addWidget(self.remove_layer_button)


        lo_bodyright.addItem(verticalSpacer)
        lo_bodyright.addWidget(layers_label)
        lo_bodyright.addLayout(lo_layers_row)
        #edit_layer_button
        #remove_layer_button
        lo_bodyright.addWidget(top_layer_label)
        lo_bodyright.addWidget(self.layers)
        lo_bodyright.addWidget(bottom_layer_label)

        lo_bodyright.addItem(verticalSpacer)
        lo_bodyright.addWidget(params_label)
        lo_bodyright.addWidget(self.theta_i)
        lo_bodyright.addWidget(self.phi_i)
        lo_bodyright.addWidget(self.energy)
        lo_bodyright.addWidget(self.screen_distance)
        
        lo_bodyright.addItem(verticalSpacer)
        lo_bodyright.addWidget(self.plotbutton)
        lo_bodyright.addItem(verticalSpacer)

        #building back out
        lo_body.addLayout(lo_bodyleft,7)
        lo_body.addLayout(lo_bodyright,3)

        #layout.addLayout(lo_header,1)
        layout.addLayout(lo_body,9)
        self.setLayout(layout)

    def new_layer(self):
        self.popup = layer_builder.LayerBuilder(self)
        self.popup.exec()

        label = self.popup.label()
        if label is not None:
            layer = custom_widgets.DragItem(label)
            layer.set_data(self.popup.values)
            self.layers.add_item(layer)

    def edit_layer(self):
        self.popup = layer_builder.LayerBuilder(self)

    def remove_layer(self):
        #make checkboxes show up
        self.popup = layer_builder.LayerRemover(self, self.layers)
        self.popup.exec()
    
    def plot(self):
        mksize = int(self.canvas.frameGeometry().width()/81)
        dim = 12
        plot_list_reg = np.full((1,3),-1.)
        plot_list_recon = np.full((1,3),-1.)
        
        all_layers = self.layers.get_item_data()
        energy = self.energy.value() * 1000.
        theta_i = self.theta_i.value()
        phi_i = self.phi_i.value()
        screen_dist = self.screen_distance.value()

        #layer_counter = 0 #use this to get decreasing intensity by lower layers
        print(all_layers) #each layer only need indicies 3, 4, 5

        for layer in all_layers:
            a_factor, b_factor, rot_factor = list(map(int, layer[3].split(" ")))
            a_sqrt, b_sqrt = layer[4]
            constants = layer[5]


            for i in range(len(constants)):
                a_recip = constants[i][0]
                b_recip = constants[i][1]
                gamma = constants[i][2]
                thetaphisets_reg = thetaphi_sets(dim,
                                            a_recip,
                                            b_recip,
                                            gamma,
                                            math.radians(theta_i),
                                            math.radians(phi_i),
                                            evtok(energy))

                a_recon = a_recip / math.sqrt(a_factor) if a_sqrt else a_recip / a_factor
                b_recon = b_recip / math.sqrt(b_factor) if b_sqrt else b_recip / b_factor            
                thetaphisets_recon = thetaphi_sets(int(dim*max(a_factor,b_factor)),
                                            a_recon,
                                            b_recon,
                                            gamma,
                                            math.radians(theta_i),
                                            math.radians(phi_i + rot_factor),
                                            evtok(energy))
                plot_list_reg = np.concatenate((plot_list_reg,thetaphisets_reg))
                plot_list_recon = np.concatenate((plot_list_recon,thetaphisets_recon))

        self.figure.clear()

        convert_to_dist = lambda angle: screen_dist * np.tan(angle)

        plot_list_dist_recon = convert_to_dist(plot_list_recon)
        plot_list_dist_reg = convert_to_dist(plot_list_reg)

        plt.gca().set_aspect('equal')
        plt.plot(plot_list_dist_recon[:,1], plot_list_dist_recon[:,0], 'ro', markersize = mksize/3)
        plt.plot(plot_list_dist_reg[:,1], plot_list_dist_reg[:,0], 'ro', markersize = mksize)
        plt.axis([-8,8,0,10])

        self.canvas.draw()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)    
    main = Window()
    main.show()
    sys.exit(app.exec())