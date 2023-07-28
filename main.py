from PyQt6 import QtCore, QtWidgets, QtGui

#plotting
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

#other imports
import sys
import math
import numpy as np

import browser
import lattice
import reconstruction
import sliders

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
            
            """if geom == "h":
                sx = x*np.sqrt(3)/2*a_recip
                sy = (y + np.abs(x%2)/2)*b_recip
            elif geom == "o" or geom == "t":
                sx = x*a_recip
                sy = y*b_recip
            elif geom == "m":
                pass #NOT YET IMPLEMENTED
            else:
                print("Surface has impromper symmetry")
                pass"""
                
            sz = delta_sz(sx, sy, theta_i, phi_i, k)
            if sz.size == 0:
                pass
            else:
                theta_f = np.arcsin(np.max(sz) / k - np.sin(theta_i))
                phi_f = np.arctan2(sy/k+np.cos(theta_i)*np.sin(phi_i), sx/k+np.cos(theta_i)*np.cos(phi_i)) - phi_i
                #print('sx',sx,'sy',sy,'phi,theta',np.degrees([phi_f, theta_f]),'index',indx)
                #arr = np.array([theta_f,phi_f])
                #real = np.array(arr)[~np.iscomplex(arr)]
                thetaphisets[indx] = np.degrees(np.array([theta_f,phi_f,1])) #last digit placeholder for intensity
                indx += 1

    return thetaphisets



#print(np.degrees(thetaphi_sets(10,20,1.89,1.89,0.03,0.15,51.2))) #k, sx, sy in angstrom^-1 (meter value / 10E10)

#main window
class Window(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setGeometry(QtCore.QRect(20, 20, 1200, 1000))
        self.setWindowTitle("RHEED Simulator")

        #create figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        #file browser
        self.browser = browser.FileBrowser()
        self.browser.lineEdit.textChanged.connect(lambda: self.load_cif())

        #reconstruction section
        self.reconstruct = reconstruction.Reconstruction()

        #slider/values
        #theta and phi are multiplied by 100
        #self.sx = sliders.CustomSlider(5,500,26, "sx") 
        #self.sy = sliders.CustomSlider(5,500,26, "sy")
        self.h = sliders.CustomSlider(0,1,1, "h")
        self.k = sliders.CustomSlider(0,1,1, "k")
        self.l = sliders.CustomSlider(0,1,1, "l")
        self.theta_i = sliders.CustomSlider(0,500,380, "theta_i") #degrees
        self.phi_i = sliders.CustomSlider(0,4500,0, "phi_i")
        self.energy = sliders.CustomSlider(10000,25000,10000, "energy") #electron-volts

        #self.sx.slider.valueChanged.connect(lambda: self.plot())
        #self.sy.slider.valueChanged.connect(lambda: self.plot())
        #self.h.slider.valueChanged.connect(lambda: self.get_cifs())
        #self.k.slider.valueChanged.connect(lambda: self.get_cifs())
        #self.l.slider.valueChanged.connect(lambda: self.get_cifs())
        self.theta_i.slider.valueChanged.connect(lambda: self.plot())
        self.phi_i.slider.valueChanged.connect(lambda: self.plot())
        self.energy.slider.valueChanged.connect(lambda: self.plot())

        #button
        #self.plot()
        self.plotbutton = QtWidgets.QPushButton('Plot')
        #self.plotbutton.clicked.connect(lambda: self.load_cif())
        self.plotbutton.clicked.connect(lambda: self.plot())
        
        
        #add widgets to window
        layout = QtWidgets.QVBoxLayout()

        #header of layout // lo stands for layout
        lo_header = QtWidgets.QHBoxLayout()
        lo_header.addWidget(self.browser)

        #body of layout
        lo_body = QtWidgets.QHBoxLayout()

        #left side of body
        lo_bodyleft = QtWidgets.QVBoxLayout()
        lo_bodyleft.addWidget(self.toolbar)
        lo_bodyleft.addWidget(self.canvas)

        #right side of body
        lo_bodyright = QtWidgets.QVBoxLayout()
        verticalSpacer = QtWidgets.QSpacerItem(15, 5, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Expanding)

        #hkl row
        lo_hklrow = QtWidgets.QHBoxLayout()
        lo_hklrow.addWidget(self.h)
        lo_hklrow.addWidget(self.k)
        lo_hklrow.addWidget(self.l)

        #lo_bodyright.addWidget(self.sx)
        #lo_bodyright.addWidget(self.sy)
        
        lo_bodyright.addItem(verticalSpacer)
        lo_bodyright.addLayout(lo_hklrow)
        lo_bodyright.addWidget(self.reconstruct)
        lo_bodyright.addItem(verticalSpacer)
        lo_bodyright.addWidget(self.theta_i)
        lo_bodyright.addWidget(self.phi_i)
        lo_bodyright.addWidget(self.energy)
        lo_bodyright.addItem(verticalSpacer)
        lo_bodyright.addWidget(self.plotbutton)
        lo_bodyright.addItem(verticalSpacer)

        #building back out
        lo_body.addLayout(lo_bodyleft,7)
        lo_body.addLayout(lo_bodyright,3)

        layout.addLayout(lo_header,1)
        layout.addLayout(lo_body,9)
        self.setLayout(layout)

    def load_cif(self):
        try:
            self.cif_file = lattice.Lattice(self.browser.get_file_name())
        except:
            print("bad file")
    
    # action called by the push button
    def plot(self):
        mksize = int(self.canvas.frameGeometry().width()/81)

        cif_values = self.cif_file.output(self.browser.get_file_name(), self.h.value(), self.k.value(), self.l.value())
        
        plot_list_reg = np.full((1,3),-1.)
        plot_list_recon = np.full((1,3),-1.)

        a_factor = float(self.reconstruct.a_change.text())
        b_factor = float(self.reconstruct.b_change.text())
        rot_factor = float(self.reconstruct.rot_change.text())

        dim = 12 #if max(a_factor,b_factor) < 8 else 60

        for i in range(len(cif_values)):
            a_recip = cif_values[i][0]
            b_recip = cif_values[i][1]
            gamma = cif_values[i][2]
            thetaphisets_reg = thetaphi_sets(dim,
                                        a_recip,
                                        b_recip,
                                        gamma,
                                        math.radians(self.theta_i.value() / 100.),
                                        math.radians(self.phi_i.value() / 100.),
                                        evtok(self.energy.value()))

            a_recon = a_recip / math.sqrt(a_factor) if self.reconstruct.is_sqrt() else a_recip / a_factor
            b_recon = b_recip / math.sqrt(b_factor) if self.reconstruct.is_sqrt() else b_recip / b_factor            
            thetaphisets_recon = thetaphi_sets(int(dim*max(a_factor,b_factor)),
                                        a_recon,
                                        b_recon,
                                        gamma,
                                        math.radians(self.theta_i.value() / 100.),
                                        math.radians(self.phi_i.value() / 100. + rot_factor),
                                        evtok(self.energy.value()))
            plot_list_reg = np.concatenate((plot_list_reg,thetaphisets_reg))
            plot_list_recon = np.concatenate((plot_list_recon,thetaphisets_recon))

        
        
        
        #dim = int(max(30,min(55,3500/(self.sx.value()+self.sy.value()))))
                      
        
        self.figure.clear()

        plt.gca().set_aspect('equal')
        plt.plot(plot_list_recon[:,1], plot_list_recon[:,0], 'ro', markersize = mksize/3)
        plt.plot(plot_list_reg[:,1], plot_list_reg[:,0], 'ro', markersize = mksize)
        plt.axis([-10,10,0,20])

        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)    
    main = Window()
    main.show()
    sys.exit(app.exec())