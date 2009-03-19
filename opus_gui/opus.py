#!/usr/bin/env python
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QIcon, QMessageBox

# General system includes
import sys, os

# Urbansim Tools
from opus_gui.main.controllers.mainwindow import OpusGui
from opus_gui.main.controllers.dialogs.message_box import MessageBox

# Main entry to program.  Set up the main app and create a new window.
def main(argv):
    # create Qt application
    app = QApplication(argv,True)

    # Setting these items allows for saving application state via a QSettings object
    app.setOrganizationName("CUSPA")
    app.setOrganizationDomain("urbansim.org")
    app.setApplicationName("OPUS")

    # Set application icon
    applicationIcon = QIcon(":/Images/Images/new-logo-medium-no-mirror.png")
    app.setWindowIcon(applicationIcon)

    # Set the app style
    # app.setStyle(QString("plastique"))

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

    # Ensure that we have an existing OPUS_HOME directory that we can write to
    valid_opus_home = True
    if not 'OPUS_HOME' in os.environ:
        msg = ('Opus GUI could not find the environment variable "OPUS_HOME".\n'
               'Opus GUI relies on this variable to function properly. '
               'Please set it to the directory containing Opus data and '
               'restart the application.')
        valid_opus_home = False
    elif not os.path.exists(os.environ['OPUS_HOME']):
        msg = ('The directory pointed to by environment variable "OPUS_HOME" '
               '("%s") appears to be missing. Please make sure that the '
               'directory pointed to by this variable is valid and restart the '
               'application.' %
               os.path.normpath(os.environ['OPUS_HOME']))
        valid_opus_home = False
    elif not os.access(os.environ['OPUS_HOME'], os.W_OK):
        msg = ('The directory pointed to by environment variable OPUS_HOME '
               '("%s") appears to be write protected (or you do not have '
               'sufficient privileges to make changes to it). Please make '
               'sure that the directory pointed to by this variable is valid '
               'and restart the application.')
        valid_opus_home = False
    if not valid_opus_home:
        QMessageBox.critical(None, 'Could not start Opus GUI',
                             msg + '\n\nOpus GUI will now quit.')
        return

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

