# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from misc.widgets import *



class ControlDataPage(QWizardPage):
    def __init__(self, parent=None):
        super(ControlDataPage, self).__init__(parent)

        self.controlHHLocationDummy = True
        self.controlPersonLocationDummy = True
        self.sourceDummy = False

        self.setTitle("Step 4: Marginal Totals")

        self.controlGroupBox = QGroupBox("""a. Will you provide the marginal totals for """
                                         """population characteristics of interest?""")
        controlWarning = QLabel("""<font color = blue>Note: If <b>No</b> is chosen, US Census Summary Files (SF) """
                               """for year 2000 will be used. </font>""")
        self.controlUserProvRadio = QRadioButton("Yes")
        self.controlAutoRadio = QRadioButton("No")
        self.controlAutoRadio.setChecked(True)
        controlHLayout = QHBoxLayout()
        controlHLayout.addWidget(self.controlUserProvRadio)
        controlHLayout.addWidget(self.controlAutoRadio)
        self.controlGroupBox.setLayout(controlHLayout)

        controlHHLocationLabel = QLabel("Select the household marginal total file")
        controlGQLocationLabel = QLabel("Select the groupquarter marginal total file")
        controlPersonLocationLabel = QLabel("Select the person marginal total file")

        self.controlHHLocationComboBox = ComboBoxFile()
        self.controlHHLocationComboBox.addItems([(""), ("Browse to select file...")])
        controlHHLocationLabel.setBuddy(self.controlHHLocationComboBox)

        self.controlGQLocationComboBox = ComboBoxFile()
        self.controlGQLocationComboBox.addItems([(""), ("Browse to select file...")])
        controlGQLocationLabel.setBuddy(self.controlGQLocationComboBox)

        self.controlPersonLocationComboBox = ComboBoxFile()
        self.controlPersonLocationComboBox.addItems([(""), ("Browse to select file...")])
        controlPersonLocationLabel.setBuddy(self.controlPersonLocationComboBox)

        controlUserProvWarning = QLabel("""<font color = blue> Note: Groupquarter data is optional; but if the person marginal"""
                                       """ totals include residents of groupquarters, then provide groupquarter information as well"""
                                       """ to generate a representative synthetic population. </font>""")
        controlUserProvWarning.setWordWrap(True)


        sourceGroupBox = QGroupBox("b. Choose the Census data source you want PopGen to use.")
        self.sourceComboBox = QComboBox()

        sourceLayout = QHBoxLayout()
        sourceLayout.addWidget(self.sourceComboBox)
        sourceGroupBox.setLayout(sourceLayout)

        self.controlUserProvGroupBox = QGroupBox("c. User provided")
        controlVLayout = QVBoxLayout()
        controlVLayout.addWidget(controlHHLocationLabel)
        controlVLayout.addWidget(self.controlHHLocationComboBox)
        controlVLayout.addWidget(controlGQLocationLabel)
        controlVLayout.addWidget(self.controlGQLocationComboBox)
        controlVLayout.addWidget(controlPersonLocationLabel)
        controlVLayout.addWidget(self.controlPersonLocationComboBox)
        self.controlUserProvGroupBox.setLayout(controlVLayout)

        self.controlUserProvGroupBox.setEnabled(False)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.controlGroupBox)
        vLayout.addWidget(controlWarning)
        vLayout.addWidget(sourceGroupBox)
        vLayout.addWidget(self.controlUserProvGroupBox)
        vLayout.addWidget(controlUserProvWarning)
        self.setLayout(vLayout)

        #self.connect(self.controlHHLocationComboBox, pyqtSignal("activated(int)"), self.controlHHCheck)
        self.controlHHLocationComboBox.activated.connect(self.controlHHCheck)
        #self.connect(self.controlGQLocationComboBox, pyqtSignal("activated(int)"), self.controlGQLocationComboBox.browseFile)
        self.controlGQLocationComboBox.activated.connect(self.controlGQLocationComboBox.browseFile)
        #self.connect(self.controlPersonLocationComboBox, pyqtSignal("activated(int)"), self.controlPersonCheck)
        self.controlPersonLocationComboBox.activatedconnect(self.controlPersonCheck)
        #self.connect(self.sourceComboBox, pyqtSignal("activated(int)"), self.sourceCheck)
        self.sourceComboBox.activatedconnect(self.sourceCheck)

        #self.connect(self.controlAutoRadio, pyqtSignal("clicked()"), self.controlAutoAction)
        self.controlAutoRadio.clicked.connect(self.controlAutoAction)
        #self.connect(self.controlUserProvRadio, pyqtSignal("clicked()"), self.controlUserProvAction)
        self.controlUserProvRadio.clicked.connect(self.controlUserProvAction)
        #self.connect(self, pyqtSignal("resolutionChanged"), self.resolutionAction)
        self.resolutionChanged.connect(self.resolutionAction)

    def resolutionAction(self, resolution):
        if resolution != 'County':
            self.sourceComboBox.clear()
            self.sourceComboBox.addItems([(""), 
                                          ("Census 2000")])
        else:
            self.sourceComboBox.clear()
            self.sourceComboBox.addItems([(""), 
                                          ("Census 2000"), 
                                          ("ACS 2005-2007")])



        if resolution == 'TAZ':
            self.controlUserProvRadio.setChecked(True)
            self.controlUserProvRadio.emit(pyqtSignal("clicked()"))
            self.controlAutoRadio.setEnabled(False)
        else:
            self.controlAutoRadio.setEnabled(True)


    def controlAutoAction(self):
        self.controlUserProvGroupBox.setEnabled(False)
        self.controlHHLocationComboBox.setCurrentIndex(0)
        self.controlGQLocationComboBox.setCurrentIndex(0)
        self.controlPersonLocationComboBox.setCurrentIndex(0)
        self.sourceComboBox.setEnabled(True)
        self.sourceComboBox.setCurrentIndex(0)
        self.controlPersonLocationDummy = True
        self.controlHHLocationDummy = True
        self.sourceDummy = False
        self.emit(pyqtSignal("completeChanged()"))

    def controlUserProvAction(self):
        self.controlUserProvGroupBox.setEnabled(True)
        if self.controlHHLocationComboBox.currentIndex() == 0:
            self.controlHHLocationDummy = False
        else:
            self.controlHHLocationDummy = True

        if self.controlPersonLocationComboBox.currentIndex() == 0:
            self.controlPersonLocationDummy = False
        else:
            self.controlPersonLocationDummy = True

        self.sourceComboBox.setEnabled(False)
        self.sourceComboBox.setCurrentIndex(0)
        self.sourceDummy = True

        self.emit(pyqtSignal("completeChanged()"))


    def controlHHCheck(self, index):
        self.controlHHLocationComboBox.browseFile(index)
        if self.controlHHLocationComboBox.currentIndex() == 0:
            self.controlHHLocationDummy = False
        else:
            self.controlHHLocationDummy = True

        self.emit(pyqtSignal("completeChanged()"))

    def controlPersonCheck(self, index):
        self.controlPersonLocationComboBox.browseFile(index)
        if self.controlPersonLocationComboBox.currentIndex() == 0:
            self.controlPersonLocationDummy = False
        else:
            self.controlPersonLocationDummy = True

        self.emit(pyqtSignal("completeChanged()"))

    def sourceCheck(self, index):
        if index>0:
            self.sourceDummy = True
        else:
            self.sourceDummy = False

        self.emit(pyqtSignal("completeChanged()"))


    def isComplete(self):
        if self.controlUserProvRadio.isChecked():
            self.sourceDummy = True
        # the code for checking the person file location still exists, the following line kinda overrides that
        # this change was made to accomodate the case where the user wants to run the synthesis using only 
        # housing variables because marginals for the person variables are not available
        self.controlPersonLocationDummy = True
        validate = self.controlHHLocationDummy and self.controlPersonLocationDummy and self.sourceDummy
        if validate:
            return True
        else:
            return False



