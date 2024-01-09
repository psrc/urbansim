# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from misc.errors import *
from misc.widgets import *


class SampleDataPage(QWizardPage):
    def __init__(self, parent=None):
        super(SampleDataPage, self).__init__(parent)

        self.sampleHHLocationDummy = True
        self.samplePersonLocationDummy = True
        self.sourceDummy = False

        self.setTitle("Step 3: Population Sample")

        self.sampleGroupBox = QGroupBox("""a. Will you provide sample data?""")
        sampleWarning = QLabel("""<font color = blue>Note: If <b>No</b> is chosen, select the US Census data source """
                               """ to use for population synthesis. Note that . </font>""")
        self.sampleUserProvRadio = QRadioButton("Yes")
        self.sampleAutoRadio = QRadioButton("No")
        self.sampleAutoRadio.setChecked(True)
        sampleHLayout = QHBoxLayout()
        sampleHLayout.addWidget(self.sampleUserProvRadio)
        sampleHLayout.addWidget(self.sampleAutoRadio)
        self.sampleGroupBox.setLayout(sampleHLayout)

        sampleHHLocationLabel = QLabel("Select the household sample file")
        sampleGQLocationLabel = QLabel("Select the groupquarter sample file")
        samplePersonLocationLabel = QLabel("Select the person sample file")

        self.sampleHHLocationComboBox = ComboBoxFile()
        self.sampleHHLocationComboBox.addItems([(""), ("Browse to select file...")])
        sampleHHLocationLabel.setBuddy(self.sampleHHLocationComboBox)

        self.sampleGQLocationComboBox = ComboBoxFile()
        self.sampleGQLocationComboBox.addItems([(""), ("Browse to select file...")])
        sampleGQLocationLabel.setBuddy(self.sampleGQLocationComboBox)

        self.samplePersonLocationComboBox = ComboBoxFile()
        self.samplePersonLocationComboBox.addItems([(""), ("Browse to select file...")])
        samplePersonLocationLabel.setBuddy(self.samplePersonLocationComboBox)

        sampleUserProvWarning = QLabel("""<font color = blue> Note: Groupquarter data is optional; but if the person control"""
                                       """ totals include residents of groupquarters, then provide groupquarter information as well"""
                                       """ to generate a representative synthetic population. </font>""")
        sampleUserProvWarning.setWordWrap(True)



        sourceGroupBox = QGroupBox("b. Choose the Census data source you want PopGen to use.")
        self.sourceComboBox = QComboBox()
        self.sourceComboBox.addItems([(""), 
                                      ("Census 2000"), 
                                      ("ACS 2005-2007")])


        sourceLayout = QHBoxLayout()
        sourceLayout.addWidget(self.sourceComboBox)
        sourceGroupBox.setLayout(sourceLayout)
        

        self.sampleUserProvGroupBox = QGroupBox("c. User provided")
        sampleVLayout = QVBoxLayout()
        sampleVLayout.addWidget(sampleHHLocationLabel)
        sampleVLayout.addWidget(self.sampleHHLocationComboBox)
        sampleVLayout.addWidget(sampleGQLocationLabel)
        sampleVLayout.addWidget(self.sampleGQLocationComboBox)
        sampleVLayout.addWidget(samplePersonLocationLabel)
        sampleVLayout.addWidget(self.samplePersonLocationComboBox)
        self.sampleUserProvGroupBox.setLayout(sampleVLayout)


        self.sampleUserProvGroupBox.setEnabled(False)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.sampleGroupBox)
        vLayout.addWidget(sampleWarning)
        vLayout.addWidget(sourceGroupBox)
        vLayout.addWidget(self.sampleUserProvGroupBox)
        vLayout.addWidget(sampleUserProvWarning)
        self.setLayout(vLayout)


        self.connect(self.sampleHHLocationComboBox, pyqtSignal("activated(int)"), self.sampleHHCheck)
        self.connect(self.sampleGQLocationComboBox, pyqtSignal("activated(int)"), self.sampleGQLocationComboBox.browseFile)
        self.connect(self.samplePersonLocationComboBox, pyqtSignal("activated(int)"), self.samplePersonCheck)
        self.connect(self.sourceComboBox, pyqtSignal("activated(int)"), self.sourceCheck)

        self.connect(self.sampleAutoRadio, pyqtSignal("clicked()"), self.sampleAutoAction)
        self.connect(self.sampleUserProvRadio, pyqtSignal("clicked()"), self.sampleUserProvAction)
        self.connect(self, pyqtSignal("resolutionChanged"), self.resolutionAction)



    def resolutionAction(self, resolution):
        if resolution == 'TAZ':
            self.sampleUserProvRadio.setChecked(True)
            self.sampleUserProvRadio.emit(pyqtSignal("clicked()"))
            self.sampleAutoRadio.setEnabled(False)
        else:
            self.sampleAutoRadio.setEnabled(True)


    def sampleAutoAction(self):
        self.sampleUserProvGroupBox.setEnabled(False)
        self.sampleHHLocationComboBox.setCurrentIndex(0)
        self.sampleGQLocationComboBox.setCurrentIndex(0)
        self.samplePersonLocationComboBox.setCurrentIndex(0)
        self.sourceComboBox.setEnabled(True)
        self.sourceComboBox.setCurrentIndex(0)
        self.sampleHHLocationDummy = True
        self.samplePersonLocationDummy = True
        self.sourceDummy = False
        self.emit(pyqtSignal("completeChanged()"))


    def sampleUserProvAction(self):
        self.sampleUserProvGroupBox.setEnabled(True)
        if self.sampleHHLocationComboBox.currentIndex() == 0:
            self.sampleHHLocationDummy = False
        else:
            self.sampleHHLocationDummy = True

        if self.samplePersonLocationComboBox.currentIndex() == 0:
            self.samplePersonLocationDummy = False
        else:
            self.samplePersonLocationDummy = True

        self.sourceComboBox.setEnabled(False)
        self.sourceComboBox.setCurrentIndex(0)
        self.sourceDummmy = True

        #print 'made true'

        self.emit(pyqtSignal("completeChanged()"))


    def sampleHHCheck(self, index):
        self.sampleHHLocationComboBox.browseFile(index)
        if self.sampleHHLocationComboBox.currentIndex() == 0:
            self.sampleHHLocationDummy = False
        else:
            self.sampleHHLocationDummy = True

        self.emit(pyqtSignal("completeChanged()"))

    def samplePersonCheck(self, index):
        self.samplePersonLocationComboBox.browseFile(index)
        if self.samplePersonLocationComboBox.currentIndex() == 0:
            self.samplePersonLocationDummy = False
        else:
            self.samplePersonLocationDummy = True

        self.emit(pyqtSignal("completeChanged()"))


    def sourceCheck(self, index):
        if index>0:
            self.sourceDummy = True
        else:
            self.sourceDummy = False

        self.emit(pyqtSignal("completeChanged()"))

        
    def isComplete(self):
        if self.sampleUserProvRadio.isChecked():
            self.sourceDummy = True
        #print self.sampleHHLocationDummy, self.samplePersonLocationDummy, self.sourceDummy
        validate = self.sampleHHLocationDummy and self.samplePersonLocationDummy and self.sourceDummy
        if validate:
            return True
        else:
            return False



