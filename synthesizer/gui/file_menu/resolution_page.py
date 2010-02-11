# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from misc.widgets import *


class ResolutionPage(QWizardPage):
    def __init__(self, parent=None):
        super(ResolutionPage, self).__init__(parent)

        self.geocorrLocationDummy = True

        self.setTitle("Step 2: Geographic Resolution")

        self.resolutionComboBox = QComboBox()
        self.resolutionComboBox.addItems([QString("County"), QString("Census Tract"),
                                          QString("Census Blockgroup"), QString("Traffic Analysis Zone (TAZ)")])
        self.resolutionComboBox.setFixedSize(QSize(250,20))

        resolutionVLayout = QVBoxLayout()
        resolutionVLayout.addWidget(self.resolutionComboBox)

        resolutionGroupBox = QGroupBox("""a. Choose the geographic resolution at which you want to"""
                                        """ synthesize the population""")
        resolutionGroupBox.setLayout(resolutionVLayout)

        resolutionWarning = QLabel("""<font color = blue> Note: If <b>TAZ</b> is chosen, all information including geographic correspondence, sample data, """
                                   """and marginal totals  must be provided by the user.</font>""")
        self.geocorrGroupBox = QGroupBox("""b. Will you provide Geographic Correspondence between the chosen geography and PUMA boundaries?""")
        self.geocorrUserProvRadio = QRadioButton("Yes")
        self.geocorrAutoRadio = QRadioButton("No")
        self.geocorrAutoRadio.setChecked(True)
        geocorrWarning = QLabel("<font color = blue> Note: If <b>No</b> is chosen, MABLE/Geocorr2K: Geographic Correspondence Engine will be used.</font>")
        
        geocorrDefLabel = QLabel("""Geographic correspondence file provides a correspondence between """
                                 """the ID of the geography and the Public Use Microdata Area (PUMA) ID"""
                                 """to which the geography belongs. See Data Structures on the Help menu"""
                                 """ option for additional information about the layout of this file.""")

        geocorrHLayout = QHBoxLayout()
        geocorrHLayout.addWidget(self.geocorrUserProvRadio)
        geocorrHLayout.addWidget(self.geocorrAutoRadio)


        self.geocorrGroupBox.setLayout(geocorrHLayout)

        geocorrLocationLabel = QLabel("Select the Geographic Correspondence file")
        self.geocorrLocationComboBox = ComboBoxFile()
        self.geocorrLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        geocorrLocationLabel.setBuddy(self.geocorrLocationComboBox)

        self.geocorrUserProvGroupBox = QGroupBox("c. User provided")
        geocorrVLayout = QVBoxLayout()
        geocorrVLayout.addWidget(geocorrLocationLabel)
        geocorrVLayout.addWidget(self.geocorrLocationComboBox)
        self.geocorrUserProvGroupBox.setLayout(geocorrVLayout)
        self.geocorrUserProvGroupBox.setEnabled(False)


        vLayout = QVBoxLayout()
        vLayout.addWidget(resolutionGroupBox)
        vLayout.addWidget(resolutionWarning)
        vLayout.addWidget(self.geocorrGroupBox)
        vLayout.addWidget(geocorrWarning)
        vLayout.addWidget(self.geocorrUserProvGroupBox)
        self.setLayout(vLayout)

        self.connect(self.geocorrAutoRadio, SIGNAL("clicked()"), self.geocorrAutoAction)
        self.connect(self.geocorrUserProvRadio, SIGNAL("clicked()"), self.geocorrUserProvAction)
        self.connect(self.geocorrLocationComboBox, SIGNAL("activated(int)"), self.fileCheck)
        self.connect(self.resolutionComboBox, SIGNAL("activated(int)"), self.resolutionAction)

    def resolutionAction(self):
        if self.resolutionComboBox.currentText() == 'Traffic Analysis Zone (TAZ)':
            self.geocorrUserProvRadio.setChecked(True)
            self.geocorrUserProvRadio.emit(SIGNAL("clicked()"))
            self.geocorrAutoRadio.setEnabled(False)
        else:
            self.geocorrAutoRadio.setEnabled(True)

    def geocorrAutoAction(self):
        self.geocorrUserProvGroupBox.setEnabled(False)
        self.geocorrLocationComboBox.setCurrentIndex(0)
        self.geocorrLocationDummy = True
        self.emit(SIGNAL("completeChanged()"))

    def geocorrUserProvAction(self):
        self.geocorrUserProvGroupBox.setEnabled(True)
        self.geocorrLocationDummy = False
        self.emit(SIGNAL("completeChanged()"))

    def fileCheck(self, index):
        self.geocorrLocationComboBox.browseFile(index)
        if self.geocorrLocationComboBox.currentIndex() == 0:
            self.geocorrLocationDummy = False
        else:
            self.geocorrLocationDummy = True
        self.emit(SIGNAL("completeChanged()"))

    def isComplete(self):
        validate = self.geocorrLocationDummy
        if validate:
            return True
        else:
            return False
