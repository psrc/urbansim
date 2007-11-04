# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Util.pythonGui import OpusPythonShell

# General system includes
import sys,string

  
# Main console class for the python console
class ConsoleBase(object):
  def __init__(self, parent):
    self.parent = parent

    self.pythonGui = OpusPythonShell(self.parent.pythonWidget,self.parent.pythonLineEdit,self.parent.__dict__)
    self.pythonLayout = QGridLayout(self.parent.pythonWidget)
    self.pythonLayout.setMargin(9)
    self.pythonLayout.setSpacing(6)
    self.pythonLayout.setObjectName("pythonLayout")
    self.pythonLayout.addWidget(self.pythonGui)
