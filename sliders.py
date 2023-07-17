from PyQt6 import QtWidgets, QtCore, QtGui

#doubleslider with upper limit of 100 and two decimal points
"""class DoubleSlider(QtWidgets.QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.decimals = 5
        self._max_int = 10 ** self.decimals

        super().setMinimum(0)
        super().setMaximum(self._max_int)

        self._min_value = 0.0
        self._max_value = 1000.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super().value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super().setValue(int((value - self._min_value) / self._value_range * self._max_int))

    def setMinimum(self, value):
        if value > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        if value < self._min_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value
    
    #def notifyValueChanged(value):
    #    return value/
    

#doubleslider with text box
class CustomSlider(QtWidgets.QWidget):
    def __init__(self, max, min, default, *args, **kwargs):
        super(CustomSlider, self).__init__(*args, **kwargs)
        self.slider = DoubleSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(default)

        self.doublebox = QtWidgets.QLineEdit()
        reg_ex_1 = QtCore.QRegExp("[0-9]+.?[0-9]{,3}") # double
        # reg_ex_2 = QRegExp("[0-9]{1,5}")  # minimum 1 integer number to maxiumu 5 integer number
        # reg_ex_3 = QRegExp("-?\\d{1,3}")  # accept negative number also
        # reg_ex_4 = QRegExp("")
        self.doublebox.setValidator(QtGui.QRegExpValidator(reg_ex_1))
        self.slider.valueChanged.connect(self.doublebox.setText)
        #self.slider.rangeChanged.connect(self.numbox.setRange)
        self.doublebox.textChanged.connect(self.slider.setValue)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.doublebox)
        layout.addWidget(self.slider)

    def getValue(self):
        return self.doublebox.text"""


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