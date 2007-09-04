#!/usr/bin/env python
#
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

# General system includes
import sys

# Urbansim Tools
from Main.opusGui import *


# Path to local QGIS install
qgis_prefix = "/usr/local"


# Main entry to program.  Set up the main app and create a new window.
def main(argv):

  # create Qt application
  app = QApplication(argv,True)
  
  # Set the app style
  app.setStyle(QString("plastique"))
  
  # initialize qgis libraries
  QgsApplication.setPrefixPath(qgis_prefix, True)
  QgsApplication.initQgis()

  # create main window
  wnd = OpusGui()
  wnd.show()

  # Create signal for app finish
  app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
  
  # Start the app up
  retval = app.exec_()
  
  # We got an exit signal so time to clean up
  QgsApplication.exitQgis()
  
  sys.exit(retval)


if __name__ == "__main__":
  main(sys.argv)

