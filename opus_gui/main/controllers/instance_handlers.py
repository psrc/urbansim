# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

# Module global instance reference to the application main window
__OPUS_GUI_INSTANCE = None

def set_opusgui_instance(opusgui):
    '''
    Sets the instance of mainwindow that is used for the access functions.
    @param opusgui (OpusGui): the instance to use
    '''
    global __OPUS_GUI_INSTANCE
    __OPUS_GUI_INSTANCE = opusgui

def __get_instance():
    ''' convenience function to avoid importing global variables everywhere '''
    global __OPUS_GUI_INSTANCE
    return __OPUS_GUI_INSTANCE

# Access functions for the main window

def get_manager_instance(manager_name):
    '''
    Get an instance handle for the named manager
    @param manager_name (String): Name of the instance to get a handle to
    (i.e 'data_manager', results_manager' etc)
    @return: the instance to the given manager or None
    '''
    instance = __get_instance()
    if instance is not None and manager_name in \
        instance.managers:
        return instance.managers[manager_name]
    return None

def get_mainwindow_instance():
    '''
    Get the instance handle for the main window.
    @return: Instance of the main window or None
    '''
    return __get_instance()

def get_db_connection_names():
    '''
    Get the global db_connection_names.
    @return: a list of connection names (list(String))
    '''
    instance = __get_instance()
    if not instance:
        return []
    else:
        return instance.db_connection_names or []

def update_mainwindow_title():
    '''
    Updates the application title for the main window to reflect any changes
    to the dirty flag.
    '''
    instance = __get_instance()
    if instance is not None:
        instance.updateWindowTitle()
