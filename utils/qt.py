from Qt import QtCore, QtGui, QtWidgets



class VerticalLine(QtWidgets.QFrame):
    
    def __init__(self):
        super(VerticalLine, self).__init__()
        
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        

class HorizontalLine(QtWidgets.QFrame):
    
    def __init__(self):
        super(HorizontalLine, self).__init__()
        
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
