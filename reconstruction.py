#separate file in case we want to implement calculation based on surface energy/DFT in the future

from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout, QCheckBox
from PyQt6.QtGui import QIntValidator

class Reconstruction(QWidget):
    #file_name = ''

    def __init__(self):
        super().__init__()
        #self.resize(800, 600)

        label1 = QLabel("Reconstruction: ")
        label2 = QLabel("x")
        label3 = QLabel("R")

        self.a_change = QLineEdit() #reconstruction along a lattice
        self.b_change = QLineEdit() #reconstruction along b lattice
        self.rot_change = QLineEdit() #in degrees

        a_valid = QIntValidator(1,11)
        b_valid = QIntValidator(1,11)
        rot_valid = QIntValidator(0,90)

        self.a_change.setValidator(a_valid)
        self.b_change.setValidator(b_valid)
        self.rot_change.setValidator(rot_valid)

        self.a_change.setText('1')
        self.b_change.setText('1')
        self.rot_change.setText('0')

        self.sqrt_box = QCheckBox("S&qrt?")

        layout = QHBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.a_change)
        layout.addWidget(label2)
        layout.addWidget(self.b_change)        
        layout.addWidget(label3)
        layout.addWidget(self.rot_change)
        layout.addWidget(self.sqrt_box)
        self.setLayout(layout)

    def is_sqrt(self):
        return self.sqrt_box.isChecked()
    
    
    """def check_val(self, input, previous, min, max):
        try:
            newval = int(input)
            if newval > min and newval < max:
                return newval
            else:
                print('Keep value of a between %i and %i'%(min,max))
        except TypeError as e:
            print('Not an integer value')
        except:
            print('bad value')
            
        return previous"""