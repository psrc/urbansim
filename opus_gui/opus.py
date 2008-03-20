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

# General system includes
import sys

# Urbansim Tools
from opus_gui.main.opusgui import *

# Main entry to program.  Set up the main app and create a new window.
def main(argv):

  # create Qt application
  app = QApplication(argv,True)
  
  # Setting these items allows for saving application state via a QSettings object
  app.setOrganizationName("CUSPA")
  app.setOrganizationDomain("urbansim.org")
  app.setApplicationName("OPUS")
  
  # Set the app style
  app.setStyle(QString("plastique"))

  # QGIS References are removed for the time being...
  #try:
  #  # QGIS bindings for mapping functions
  #  import qgis.core
  #  # Path to local QGIS install
  #  qgis_prefix = "/usr/local/qgis_svn"
  #  # initialize qgis libraries
  #  qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
  #  qgis.core.QgsApplication.initQgis()
  #except ImportError:
  #    print "Unable to import QGIS"

  # create main window
  wnd = OpusGui()
  wnd.show()

  # Create signal for app finish
  app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

  # Start the app up
  retval = app.exec_()

  # QGIS References are removed for the time being...
  #try:
  #  import qgis.core
  #  # We got an exit signal so time to clean up
  #  qgis.core.QgsApplication.exitQgis()
  #except ImportError:
  #  pass

  sys.exit(retval)


if __name__ == "__main__":
  main(sys.argv)

