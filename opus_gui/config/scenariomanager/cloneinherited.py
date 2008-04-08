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

from opus_gui.config.scenariomanager.cloneinherited_ui import Ui_CloneInheritedGui

import random

class CloneInheritedGui(QDialog, Ui_CloneInheritedGui):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent.mainwindow, fl)
        self.setupUi(self)
        self.parent = parent
        # Add in the base XML for user to select the drop point
    
    def on_createXML_released(self):
        # Clone the node and drop it in...
        self.close()

    def on_cancelXML_released(self):
        # Close things up...
        self.close()

