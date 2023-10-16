#separate file in case we want to implement calculation based on surface energy/DFT in the future
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QCheckBox
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt

class Reconstruction(QWidget):
    #file_name = ''

    def __init__(self,abrot=None):
        super().__init__()
        #self.resize(800, 600)

        if abrot is None:
            abrot = ["1","1","0"]

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

        self.a_change.setText(abrot[0])
        self.b_change.setText(abrot[1])
        self.rot_change.setText(abrot[2])

        self.sqrt_box_a = QCheckBox("S&qrt?")
        self.sqrt_box_b = QCheckBox("S&qrt?")

        layout = QGridLayout()
        layout.addWidget(label1,0,0)
        layout.addWidget(self.a_change,0,1)
        layout.addWidget(label2,0,2)
        layout.addWidget(self.b_change,0,3)        
        layout.addWidget(label3,0,4)
        layout.addWidget(self.rot_change,0,5)
        layout.addWidget(self.sqrt_box_a,1,1,Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.sqrt_box_b,1,3,Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def is_a_sqrt(self):
        return self.sqrt_box_a.isChecked()
    
    def is_b_sqrt(self):
        return self.sqrt_box_b.isChecked()
    
    #returns a, b, and rotation factors in "a b rot" format
    def value(self):
        return "%s %s %s" %(self.a_change.text(), self.b_change.text(), self.rot_change.text())
    
    #returns True if all inputs are valid
    def is_valid(self):
        return self.a_change.hasAcceptableInput() & self.b_change.hasAcceptableInput() & self.rot_change.hasAcceptableInput()
    
    
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