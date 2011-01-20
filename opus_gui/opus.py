#!/usr/bin/env python
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
# PyQt4 includes for python bindings to QT

from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QIcon, QMessageBox

# General system includes
import sys, os

# Urbansim Tools
from opus_gui.main.controllers.opus_gui_configuration import OpusGuiConfiguration

# importing OpusGui could take a long time, so we want to load the configuration and display the
# splash-screen meanwhile

gui_config = None

def load_gui():
    global gui_config
    # create Qt application
    app = QApplication(sys.argv,True)
    gui_config = OpusGuiConfiguration()
    gui_config.app = app
    gui_config.load()
    gui_config.splash_screen.show()
    gui_config.splash_screen.raise_()
    gui_config.splash_screen.activateWindow()
    gui_config.splash_screen.showMessage('Loading and compiling Python Modules...')
    gui_config.splash_screen.show()

if __name__ == '__main__':
    load_gui() # start loading the gui before doing the heavy imports

from opus_gui.main.controllers.mainwindow import OpusGui

# Main entry to program.  Set up the main app and create a new window.
def main():
    global gui_config
    if gui_config is None:
        load_gui()
    app = gui_config.app
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

    # init main window
    gui_config.splash_screen.showMessage('Initializing Opus Main Window...')
    wnd = OpusGui(gui_configuration = gui_config)
    gui_config.splash_screen.finish(wnd)

    wnd.show()
    wnd.raise_()
    wnd.activateWindow()

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
    main()

