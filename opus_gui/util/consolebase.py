# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 


# PyQt4 includes for python bindings to QT
from PyQt4.QtGui import QGridLayout

from opus_gui.util.pythongui import OpusPythonShell

# Main console class for the python console
class ConsoleBase(object):
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

        self.pythonGui = OpusPythonShell(self.mainwindow.pythonWidget,self.mainwindow.pythonLineEdit,self.mainwindow.__dict__)
        self.pythonLayout = QGridLayout(self.mainwindow.pythonWidget)
        self.pythonLayout.setMargin(9)
        self.pythonLayout.setSpacing(6)
        self.pythonLayout.setObjectName("pythonLayout")
        self.pythonLayout.addWidget(self.pythonGui)
