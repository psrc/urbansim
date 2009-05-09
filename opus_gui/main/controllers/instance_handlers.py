# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

'''
Provides access functions to get instance references of the currently active
main window.

Functions of most general interest:

    get_manager_instance(manager_name)
        Fetches a reference to any of the loaded managers or None if no such
        manager exists.

    update_window_title()
        Updates the title of the main window to reflect any changes to the
        dirty state of the project.

    get_db_connection_names()
        Retrieve a list of names for database connections that are configured
        in the Database Manager.

'''

# Instance of the application main window
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
    @return: the instance of the given manager or None
    '''
    instance = __get_instance()
    if instance is not None and manager_name in instance.managers:
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

def update_mainwindow_savestate():
    '''
    Updates the application title for the main window to reflect any changes
    to the dirty flag.
    '''
    instance = __get_instance()
    if instance is not None:
        instance.update_saved_state()
