from PyQt6 import QtWidgets, QtCore, QtGui

#doubleslider with given limits and two decimal points
class DoubleSlider(QtWidgets.QSlider):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = 10. ** 1 #one decimal point
        self.setValue(0)

        self._min_value = 0
        self._max_value = 1000 #real max is 100.0

        super().valueChanged.connect(self.new_val)

    """@property
    def _value_range(self):
        return self._max_value - self._min_value"""

    def value(self):
        return float(super().value()) / self.decimals

    #input a float
    def setValue(self, value):
        super().setValue(int(value * self.decimals))
        self.valueChanged.emit(value)

    #input a float
    def setMinimum(self, value):
        val = value*self.decimals
        if val > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = val
        super().setMinimum(int(val))

    #input a float
    def setMaximum(self, value):
        val = value*self.decimals
        if val < self._min_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._max_value = val
        super().setMaximum(int(val))

    def minimum(self):
        return self._min_value / self.decimals

    def maximum(self):
        return self._max_value / self.decimals
    
    def new_val(self, int_val):
        self.setValue(float(int_val) / self.decimals)

    

#doubleslider with text box
class CustomDoubleSlider(QtWidgets.QWidget):
    def __init__(self, min, max, default, name, *args, **kwargs):
        super(CustomDoubleSlider, self).__init__(*args, **kwargs)
        self.slider = DoubleSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(default)

        self.name_label = QtWidgets.QLabel(name)
        self.name_label.setFixedWidth(115)
        self.lower_limit_label = QtWidgets.QLabel(str(min))
        self.upper_limit_label = QtWidgets.QLabel(str(max))

        self.doublebox = QtWidgets.QLineEdit()
        self.doublebox.setFixedWidth(30)
        valid = QtGui.QDoubleValidator(float(min), float(max), 1)
        self.doublebox.setValidator(valid)
        self.doublebox.setText(str(default))

        self.slider.valueChanged.connect(self.changeText)
        #self.slider.rangeChanged.connect(self.numbox.setRange)
        self.doublebox.textChanged.connect(self.changeSlider)
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.doublebox)
        layout.addWidget(self.lower_limit_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.upper_limit_label)

    def value(self):
        return float(self.doublebox.text())
    
    def changeText(self, value):
        self.doublebox.setText(str(value))
    
    def changeSlider(self, text):
        if self.doublebox.hasAcceptableInput():
            self.slider.setValue(float(text))


class CustomSlider(QtWidgets.QWidget):
    valueChanged = QtCore.pyqtSignal()

    def __init__(self, min, max, val, name, *args, **kwargs):
        super(CustomSlider, self).__init__(*args, **kwargs)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.numbox = QtWidgets.QSpinBox()
        self.label = QtWidgets.QLabel(name)

        self.slider.valueChanged.connect(self.numbox.setValue)
        self.slider.rangeChanged.connect(self.numbox.setRange)
        self.numbox.valueChanged.connect(self.slider.setValue)
        
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setRange(min, max)
        self.slider.setValue(val)
        self.numbox.setRange(self.slider.minimum(), self.slider.maximum())
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.numbox)
        layout.addWidget(self.slider)

    @QtCore.pyqtSlot(int)
    def setMinimum(self, minval):
        self.slider.setMinimum(minval)

    @QtCore.pyqtSlot(int)
    def setMaximum(self, maxval):
        self.slider.setMaximum(maxval)

    @QtCore.pyqtSlot(int, int)
    def setRange(self, minval, maxval):
        self.slider.setRange(minval, maxval)

    @QtCore.pyqtSlot(int)
    def setValue(self, value):
        self.slider.setValue(value)

    def setValue(self, value):
        if value != value():
            self.slider.setValue(value)
            self.valueChanged.emit(value)

    #def valueChangedEvent (self):
    #    if self.slider.valueChanged:
    #       self.valueChanged.emit()


    def value(self):
        return self.slider.value()
    


#Browser for files
class FileBrowser(QtWidgets.QWidget):
    #file_name = ''

    def __init__(self):
        super().__init__()
        #self.resize(800, 600)

        self.file_name = ""

        self.button1 = QtWidgets.QPushButton('Open File')
        #self.labelImage = QLabel()
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setReadOnly(True)

        self.button1.clicked.connect(self.get_folder)       

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def get_folder(self):
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Project Data', r"", "")
        self.lineEdit.setText(self.get_file_name())
        #print(self.get_file_name())

    def get_file_name(self):
        return self.file_name

class DragItem(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(25, 5, 25, 5)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        # Store data separately from display label, but use label for default.
        self.label = self.text()
        self.data = self.text()

    def set_data(self, data):
        self.data = data

    def mouseMoveEvent(self, e):

        if e.buttons() == QtCore.Qt.MouseButton.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            drag.setMimeData(mime)

            pixmap = QtGui.QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(QtCore.Qt.DropAction.MoveAction)


class DragWidget(QtWidgets.QWidget):
    """
    Generic list sorting handler.
    """

    orderChanged = QtCore.pyqtSignal(list)

    def __init__(self, *args, orientation=QtCore.Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        # Store the orientation for drag checks later.
        self.orientation = orientation

        if self.orientation == QtCore.Qt.Orientation.Vertical:
            self.blayout = QtWidgets.QVBoxLayout()
        else:
            self.blayout = QtWidgets.QHBoxLayout()

        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.position()
        widget = e.source()

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if self.orientation == QtCore.Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = pos.y() < w.y() #+ w.size().height() // 2
            else:
                # Drag drop horizontally.
                drop_here = pos.x() < w.x() #+ w.size().width() // 2

            if drop_here:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.blayout.insertWidget(n-1, widget)
                self.orderChanged.emit(self.get_item_data())
                break
            elif n == self.blayout.count()-1:
                self.blayout.insertWidget(n,widget)
                self.orderChanged.emit(self.get_item_data())

        e.accept()

    def add_item(self, item):
        self.blayout.addWidget(item)

    def remove_item(self, index):
        w = self.blayout.itemAt(index).widget()
        w.setParent(None)

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            data.append(w.data)
        return data
    
    def get_item_labels(self):
        labels = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            labels.append(w.label)
        return labels


"""class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drag = DragWidget(orientation=Qt.Orientation.Vertical)
        for n, l in enumerate(['A', 'B', 'C', 'D']):
            item = DragItem(l)
            item.set_data(n)  # Store the data.
            self.drag.add_item(item)

        # Print out the changed order.
        # self.drag.orderChanged.connect(print)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.drag)
        layout.addStretch(1)
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication([])
w = MainWindow()
w.show()

app.exec()"""
