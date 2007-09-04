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

# QGIS bindings for mapping functions
from qgis.core import *
from qgis.gui import *

# Custom Tools

# UI specific includes
from opusMain_ui import Ui_MainWindow

# General system includes
import sys

  
# Main window used for houseing the canvas, toolbars, and dialogs
class OpusGui(QMainWindow, Ui_MainWindow):

  def __init__(self):
    QMainWindow.__init__(self)

    # required by Qt4 to initialize the UI
    self.setupUi(self)

    # We need to initialize the window sizes
    self.splitter.setSizes([150,700])
