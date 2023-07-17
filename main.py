from PyQt5 import QtCore, QtWidgets, QtGui

#cif reader
from pymatgen.io.cif import CifParser
from pymatgen.core import structure as pgStructure
from pymatgen.core.operations import SymmOp
from pymatgen.core.lattice import Lattice

#plotting
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

#other imports
import sys
import math
import numpy as np
import sliders

#all angles in radians by default
def cif_read(self):

    #Read CIF file
    self.chooseCif = QtWidgets.QWidget()
    self.chooseCifGrid = QtWidgets.QGridLayout(self.chooseCif)
    self.chooseCifBrowser = browser.Browser(self.chooseCif, {"*.cif","*.CIF"})
    self.chooseCifLabel = QtWidgets.QLabel("The path of the CIF file is:\n")
    self.chooseCifLabel.setAlignment(QtCore.Qt.AlignTop)
    self.chooseCifLabel.setWordWrap(True)
    self.chooseCifButton = QtWidgets.QPushButton("Add CIF")
    self.chooseCifButton.clicked.connect(self.get_cif_path)
    self.chooseCifGrid.addWidget(self.chooseCifBrowser,0,0)
    self.chooseCifGrid.addWidget(self.chooseCifLabel,1,0)
    self.chooseCifGrid.addWidget(self.chooseCifButton,2,0)
    self.chooseCifBrowser.FILE_DOUBLE_CLICKED.connect(self.set_cif_path)


#convert energy in eVs to wavenumber in A^-1
def evtok(energy_evs):
    return 0.5123*math.sqrt(energy_evs)

#input and output vectors
def determineReciprocal(a_real, b_real):

    return 

#magnitude of a vector
def magnitude(vec):
    return np.linalg.norm(vec)

#quadratic solve for sz
def delta_sz(sx,sy, theta_i, phi_i, k):
    a = 1
    b = -2*k*np.sin(theta_i) #must be in radians
    c = pow(sx,2) + pow(sy,2) +2*k*np.cos(theta_i)*(sx*np.cos(phi_i)+sy*np.sin(phi_i))
    roots = np.roots([a,b,c])
    return np.array(roots)[~np.iscomplex(roots)]
    #print('sx',sx,'sy',sy,'result',result)

#solve for theta and phi final values
def thetaphi_sets(n, m, delta_sx, delta_sy, theta_i, phi_i, k):
    thetaphisets = np.full((n*m,2),-1.)
    degreesphi = int(np.degrees(phi_i))
    indx = 0
    for x in range(-(int (2*n/3)),int ((n+1)/2)): #start from farthest point go back toward specular
        for y in range(-(int (m/2))+degreesphi,int ((m+1)/2) + degreesphi): #start from one side sweep to other, origin at middle
            sx = x*delta_sx - y*delta_sy/2
            sy = y*delta_sy*np.sqrt(3)/2
            sz = delta_sz(sx, sy, theta_i, phi_i, k)
            if sz.size == 0:
                pass
            else:
                theta_f = np.arcsin(np.max(sz) / k - np.sin(theta_i))
                phi_f = np.arctan2(sy/k+np.cos(theta_i)*np.sin(phi_i), sx/k+np.cos(theta_i)*np.cos(phi_i))
                print('sx',sx,'sy',sy,'phi,theta',np.degrees([phi_f, theta_f]),'index',indx)
                #arr = np.array([theta_f,phi_f])
                #real = np.array(arr)[~np.iscomplex(arr)]
                thetaphisets[indx] = np.array([theta_f,phi_f])
                indx += 1

    return thetaphisets



#print(np.degrees(thetaphi_sets(10,20,1.89,1.89,0.03,0.15,51.2))) #k, sx, sy in angstrom^-1 (meter value / 10E10)

#main window
class Window(QtWidgets.QDialog):

    mksize = 5

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)


        self.setGeometry(QtCore.QRect(20, 20, 900, 700))
        self.setWindowTitle("RHEED Simulator")

        #create figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        #slider/values
        self.sx = sliders.CustomSlider(0,1000,26, "sx") #all numbers, except energy, multiplied by 100
        self.sy = sliders.CustomSlider(0,1000,26, "sy")
        self.theta_i = sliders.CustomSlider(0,500,270, "theta_i") #degrees
        self.phi_i = sliders.CustomSlider(0,9000,0, "phi_i")
        self.energy = sliders.CustomSlider(10000,25000,16000, "energy") #electron-volts

        #button
        self.refresh(
            15,
            50,
            float(self.sx.value())/100.,
            float(self.sy.value())/100.,
            math.radians(self.theta_i.value() / 100.),
            math.radians(self.phi_i.value() / 100.),
            evtok(self.energy.value()))
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(
            lambda: self.refresh(
                        45,
                        100,
                        float(self.sx.value())/100.,
                        float(self.sy.value())/100.,
                        math.radians(self.theta_i.value() / 100.),
                        math.radians(self.phi_i.value() / 100.),
                        evtok(self.energy.value())))
        
        #add widgets to window
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.sx)
        layout.addWidget(self.sy)
        layout.addWidget(self.theta_i)
        layout.addWidget(self.phi_i)
        layout.addWidget(self.energy)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        #layout.addWidget()
        layout.addWidget(self.button)
        self.setLayout(layout)
  
    #update the window
    def refresh(self, n, m, delta_sx, delta_sy, theta_i, phi_i, k):
        print ('start here')
        global mksize
        mksize = int(self.canvas.frameGeometry().width()/324)
        self.plot(n, m, delta_sx, delta_sy, theta_i, phi_i, k)

    
    # action called by the push button
    def plot(self, n, m, delta_sx, delta_sy, theta_i, phi_i, k):
        
        thetaphisets = np.degrees(thetaphi_sets(n, m, delta_sx, delta_sy, theta_i, phi_i, k))
        degreephi = np.degrees(phi_i)

        self.figure.clear()

        plt.gca().set_aspect('equal')
        plt.plot(thetaphisets[:,1], thetaphisets[:,0], 'ro', markersize = mksize)
        plt.axis([-5+degreephi,5+degreephi,0,10])

        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)    
    main = Window()
    main.show()
    sys.exit(app.exec_())