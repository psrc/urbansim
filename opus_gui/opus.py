#!/usr/bin/env python
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
# PyQt4 includes for python bindings to QT

from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QIcon, QMessageBox

# General system includes
import sys, os

# Ensure that we have an existing OPUS_HOME directory that we can write to
def check_opus_home():
    valid_opus_home = False
    try:
        from opus_core.paths import OPUS_HOME
    except Exception as e:
        msg = 'Could not import "paths" module from "opus_core".\n%s\n\n' \
            'Please make sure that the PYTHONPATH environment variable is set to the location of the "src" directory.' % e
    else:
        if not os.path.exists(OPUS_HOME):
            msg = 'The directory pointed to by environment variable "OPUS_HOME" '\
            '("%s") appears to be missing. Please make sure that the '\
            'directory pointed to by this variable is valid and restart the '\
            'application.' % OPUS_HOME
        elif not os.access(OPUS_HOME, os.W_OK):
            msg = 'The Opus home directory '\
            '("%s") appears to be write protected (or you do not have '\
            'sufficient privileges to make changes to it). Please make '\
            'sure that this directory is valid, '\
            'or set the "OPUS_HOME" environment variable to another location, '\
            'and restart the application.'
        else:
            valid_opus_home = True

    if not valid_opus_home:
        QMessageBox.critical(None, 'Could not start Opus GUI', msg + '\n\nOpus GUI will now quit.')
    
    return valid_opus_home

# importing OpusGui could take a long time, so we want to load the configuration and display the
# splash-screen meanwhile

gui_config = None

def load_gui():
    global gui_config
    if not gui_config is None:
        return
    
    # create Qt application
    app = QApplication(sys.argv,True)

    # Do this first, because loading the gui_config requires OPUS_HOME
    if not check_opus_home():
        sys.exit(1)

    # Urbansim Tools
    from opus_gui.main.controllers.opus_gui_configuration import OpusGuiConfiguration
    gui_config = OpusGuiConfiguration()
    gui_config.app = app
    
    gui_config.load()
    gui_config.splash_screen.show()
    gui_config.splash_screen.raise_()
    gui_config.splash_screen.activateWindow()
    gui_config.splash_screen.showMessage('Loading and compiling Python Modules...')
    gui_config.splash_screen.show()

# Main entry to program.  Set up the main app and create a new window.
def main():
    load_gui() # start loading the gui before doing the heavy imports
    
    global gui_config
    assert gui_config is not None
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

    # init main window
    gui_config.splash_screen.showMessage('Initializing Opus Main Window...')
    from opus_gui.main.controllers.mainwindow import OpusGui
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

