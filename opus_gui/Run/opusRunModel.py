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
from opusRunModel_ui import *
import sys

class RunModelGui(QDialog, Ui_OpusRunModel):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
        self.parent = parent

    def on_pbnRunModel_released(self):
	# Fire up a new thread and run the model
	1+1
            
    def on_pbnCancel_released(self):
        self.close()

