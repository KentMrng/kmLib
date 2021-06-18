

from Qt import QtCore, QtGui, QtWidgets

from qtUtils import Constants
from qtUtils import Style



class SpacerTypes(object):
    """Utility object for defining types of Spacers."""
    VERTICAL = (QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Expanding)
    HORIZONTAL = (QtWidgets.QSizePolicy.Expanding,
                  QtWidgets.QSizePolicy.Minimum)
    MINIMUM = (QtWidgets.QSizePolicy.Minimum,
               QtWidgets.QSizePolicy.Minimum)
    MAXIMUM = (QtWidgets.QSizePolicy.Maximum,
               QtWidgets.QSizePolicy.Maximum)
    FIXED = (QtWidgets.QSizePolicy.Fixed,
             QtWidgets.QSizePolicy.Fixed)


class LabelLineEdit(QtWidgets.QWidget):
    """Container widget that contains a lineedit and label."""
    def __init__(self, labelText=None, defaultText='', tooltip=None, validators=None, completers=None, parent=None):
        super(LabelLineEdit, self).__init__(parent=parent)
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setVerticalSpacing(0)
        self.label = QtWidgets.QLabel(labelText)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.lineEdit = LineEdit(defaultText, completerStrings=completers)
        # self.lineEdit = QtWidgets.QLineEdit(defaultText)
        self.lineEdit.setToolTip(tooltip)
        self.horizontalLine = HLine()
        self.valicators = validators or []
        self.setupUi()
        self.setupConnections()
        self.setAutoFillBackground(True)
    
    def setupUi(self):
        """Creates the widget layout."""
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.lineEdit, 1, 0, 1, 4)
        self.mainLayout.addWidget(self.horizontalLine, 2, 0, 1, 4)
        # self.label.setStyleSheet(Style.LABEL_TEXT)

    def setupConnections(self):
        self.lineEdit.textChanged.connect(self.validateText)
        self.lineEdit.focusChange.connect(self.textFocusChange)
    
    def setText(self, text):
        self.lineEdit.setText(text)
    
    def textFocusChange(self, value):
        """Highlight the underline when in focus"""
        if value:
            pass
            # self.horizontalLine.setStyleSheet(Style.UNDERLINE_HIGHLIGHT)
        else:
            pass
            # self.horizontalLine.setStyleSheet(Style.UNDERLINE)
    
    def validateText(self):
        """Check validators add set the style of the label."""
        results = [i(self.lineEdit.text()) for i in self.validators]
        if all(results):
            # self.label.setStyleSheet(Style.LABEL_TEXT)
            return True
        # self.label.setStyleSheet(Style.INVALID_TEXT)
        return False
    
    def text(self):
        return self.lineEdit.text()


class LineEdit(QtWidgets.QLineEdit):
    """Wrapper around QLineEdit that arrows for changing text with up/down arrow keys."""
    focusChange = QtCore.Signal(bool)
    
    def __init__(self, defaultText=None, completerStrings=None, parent=None):
        super(LineEdit, self).__init__(parent=parent)
        self.setText(defaultText)
        self.index = -1
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.completer = QtWidgets.QCompleter()
        try:
            self.completerModel = QtCore.QStringListModel()
        except:
            self.completerModel = QtGui.QStringListModel()
        self.completerStrings = completerStrings or []
        self.setupCompleter()
        # self.setStyleSheet(Style.LINE_EDIT)
    
    def focusInEvent(self, e):
        super(LineEdit, self).focusInEvent(e)
        self.focusChange.emit(True)
    
    def focusOutEvent(self, e):
        super(LineEdit, self).focusInEvent(e)
        self.focusChange.emit(False)
    
    def setupCompleter(self):
        """Add completer items"""
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completerModel.setStringList(self.completerStrings)
        self.completer.setModel(self.completerModel)
        # self.completer.popup().setStyleSheet(Style.POPUP_LIST_VIEW)
        self.setCompleter(self.completer)
    
    def keyPressEvent(self, event):
        """Add up and down arrow key events to built in functionality."""
        keyPressed = event.key()
        if keyPressed in [Constants.UP_KEY, Constants.DOWN_KEY, Constants.TAB_KEY]:
            self.index = max(0, self.index - 1)
        elif keyPressed == Constants.DOWN_KEY:
            self.index = min(len(self.completerStrings) - 1, self.index + 1)
        elif keyPressed == Constants.TAB_KEY and self.completerStrings:
            self.tabPressed()
        if self.completerStrings:
            self.setTextToCompleterIndex()
        super(LineEdit, self).keyPressEvent(event)
    
    def setTextToCompleterIndex(self):
        """Set the current text to current index of the completers."""
        self.setText(self.completerStrings[self.index])
    
    def tabPressed(self):
        """Action called with the tab key is pressed.
        Completes the string based on the completers.
        """
        current_text = self.text()
        matches = [i for i in self.completerStrings if i.startswith(current_text)]
        if matches:
            self.setText(matches[0])


class SelectPulldown(QtWidgets.QWidget):
    pass
    
class SpacerItem(QtWidgets.QSpacerItem):
    """A utility SpacerItem that simplifies the creation of QSpacerItems."""
    
    def __init__(self, spacerType, width=20, height=40):
        super(SpacerItem, self).__init__(width, height, spacerType[0], spacerType[1])


class LabelToggle(QtWidgets.QWidget):
    pass

class Toggle(QtWidgets.QSlider):
    pass

class HelpWidget(QtWidgets.QWidget):
    pass

class HelpButton(QtWidgets.QPushButton):
    pass


class HLine(QtWidgets.QFrame):
    """A simple horizontal line."""
    
    def __init__(self):
        super(HLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setAccessibleName = 'horizontalLine'
        












