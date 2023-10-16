from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QVBoxLayout, QDialog, QLabel, QPushButton, QSpacerItem, QSizePolicy, QErrorMessage, QMessageBox
from PyQt6.QtCore import QRect
from pathlib import Path

import custom_widgets, lattice, reconstruction

class LayerBuilder(QDialog):
    def __init__(self, parent, vals=None):
        super().__init__(parent)
        
        #values stored as list of (0) layer type, (1) file_name, (2) Miller indices, (3) reconstruction, (4) sqrt in reconstructions, (5) the slabs
        if vals is None:
            vals = ["Add Layer",
                      "",
                      "0 0 1",
                      "1 1 0",
                      [False, False],
                      None]
        self.values = vals
        #self.setGeometry(QRect(200, 200, 350, 300))
        self.setWindowTitle(self.values[0])

        hkl = self.values[2].split()
        abrot = self.values[3].split()

        self.browser = custom_widgets.FileBrowser()
        self.h = custom_widgets.CustomSlider(0,3,int(hkl[0]), "h")
        self.k = custom_widgets.CustomSlider(0,3,int(hkl[1]), "k")
        self.l = custom_widgets.CustomSlider(0,3,int(hkl[2]), "l")
        self.reconstruct = reconstruction.Reconstruction(abrot)
        #self.color_label = QLabel("Plot color: ")
        #self.colors = QComboBox()
        #self.colors.addItems(['Red','Blue','Green','Magenta','Cyan','Yellow'])
        self.button = QPushButton("Confirm")
        self.button.clicked.connect(self.output)

        layout = QVBoxLayout()
        verticalSpacer = QSpacerItem(2, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        lo_hklrow = QHBoxLayout()
        lo_hklrow.addWidget(self.h)
        lo_hklrow.addWidget(self.k)
        lo_hklrow.addWidget(self.l)

        lo_colorrow = QHBoxLayout()
        lo_colorrow.addWidget

        layout.addWidget(self.browser)
        layout.addLayout(lo_hklrow)
        layout.addWidget(self.reconstruct)
        #layout.addWidget(self.colors)
        layout.addSpacerItem(verticalSpacer)
        layout.addWidget(self.button)
        layout.addSpacerItem(verticalSpacer)

        self.setLayout(layout)

    #returns a nice label that include material, Miller indices, and reconstruction
    def label(self):
        if self.values[1] != "":
            file_name = Path(self.values[1]).stem
            miller_indices = self.values[2].replace(" ","")
            reconstruction_vals = self.values[3].split(" ")
            sqrts = self.values[4]
            reconstruct_a = "sqrt"+reconstruction_vals[0] if sqrts[0] else reconstruction_vals[0]
            reconstruct_b = "sqrt"+reconstruction_vals[1] if sqrts[1] else reconstruction_vals[1]
            rotation = "R"+reconstruction_vals[2] if int(reconstruction_vals[2])!=0 else ""

            return "%s(%s)-%sx%s%s" %(file_name, miller_indices, reconstruct_a, reconstruct_b, rotation)
        else:
            return None


    #store all values and return
    def output(self):
        #instance variables
        file_name = self.browser.get_file_name()
        h = self.h.value()
        k = self.k.value()
        l = self.l.value()
        cif_file = lattice.Lattice(file_name)

        #check validity of inputs
        miller_check = not (h == k == l == 0)
        reconstruction_check = self.reconstruct.is_valid()
        file_check = cif_file.valid_file
        slab_check = True

        if miller_check & reconstruction_check & file_check:
            hkl_str = "%d %d %d" %(h, k, l)

            slabs = cif_file.output(file_name, h, k, l)
            slab_check = cif_file.valid_slabs

            if slab_check:
                self.values = ["Edit layer",
                                file_name,
                                hkl_str,
                                self.reconstruct.value(),
                                [self.reconstruct.is_a_sqrt(), self.reconstruct.is_b_sqrt()],
                                slabs]
                
                self.close()
                return

        mill_error = "" if miller_check else "Miller indices must not be (000)\n"
        recons_error = "" if reconstruction_check else "Reconstruction values not valid\n"
        file_error = "" if file_check else "Error in file or file name"
        slab_error = "" if slab_check else "Cannot make slabs with current file and Miller indices"


        
        """msg = QMessageBox(self)
        msg.critical(self,"Error", mill_error + recons_error + file_error + slab_error)
        msg.exec()"""

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Fix the following error(s)")
        msg.setInformativeText(file_error + mill_error + recons_error + slab_error)
        msg.setWindowTitle("Error")
        msg.exec()
        """self.error_popup = QErrorMessage(self)
        self.error_popup.showMessage(mill_error + recons_error + file_error + slab_error)
        self.error_popup.exec()"""

    def value(self):
        return self.values
    

class LayerRemover(QDialog):

    #layers should be Drag Widget, edit is boolean whether editing or removing
    def __init__(self, parent, drag_widget_layers=None, edit = False):
        super().__init__(parent)
        self.setWindowTitle("Edit Layer" if edit else "Remove Layer")

        self.layers = drag_widget_layers
        labels = self.layers.get_item_labels()

        if labels == []:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("There are no layers to %s" %("edit" if edit else "remove"))
            msg.setInformativeText("Add a layer first with \'Add Layer\' button")
            msg.setWindowTitle("No layers")
            msg.exec()
        else:

            layout = QVBoxLayout()

            top_row = QHBoxLayout()
            
            check_boxes = []

            for label_text in labels:
                row = QHBoxLayout()
                checkBox = QCheckBox()
                check_boxes.append(check_boxes) #this might not work!!
                label = QLabel(label_text)
                row.addWidget(checkBox)
                row.addWidget(label)
                layout.addLayout(row)



            remove_button = QPushButton("Confirm")
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(self.close)


            button_row = QHBoxLayout()
            button_row.addWidget(remove_button)
            button_row.addWidget(cancel_button)

            layout.addLayout(button_row)

            self.setLayout(layout)

    def remove(self):

        return self.layers
        