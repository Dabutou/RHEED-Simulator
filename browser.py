import sys
from PyQt6.QtWidgets import QWidget, QFileDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout

#need to remove user's editing privileges of lineEdit
class FileBrowser(QWidget):
    #file_name = ''

    def __init__(self):
        super().__init__()
        #self.resize(800, 600)

        self.file_name = ""

        self.button1 = QPushButton('Open File')
        #self.labelImage = QLabel()
        self.lineEdit = QLineEdit()
        self.lineEdit.setReadOnly(True)

        self.button1.clicked.connect(self.get_folder)       

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        #layout.addWidget(self.labelImage)
        #layout.addWidget(self.button2)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def get_folder(self):
        self.file_name, _ = QFileDialog.getOpenFileName(
            self, 'Project Data', r"", "")
        self.lineEdit.setText(self.get_file_name())
        #print(self.get_file_name())

    def get_file_name(self):
        return self.file_name
