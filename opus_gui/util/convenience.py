# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import SIGNAL, QObject
from PyQt4.QtGui import QAction
from opus_gui.util.icon_library import IconLibrary

def create_qt_action(icon_name, text, callback, parent_qt_object):
    '''
    Convenience method to create actions.
    @param icon_name (str) name of icon to use
    @param text (str) action label
    @param callback (function) callback function to call when triggered (no parameters)
    @param parent_qt_object (QObject) parent object of action
    @return: the created action (QAction)
    '''
    action = QAction(IconLibrary.icon(icon_name), text, parent_qt_object)
    QObject.connect(action, SIGNAL('triggered()'), callback)
    return action

def get_unique_name(base_name, list_of_current_names):
    '''
    Get a unique name based on the base_name
    @param base_name (str) the preferred name
    @param list_of_current_names (list(str)) the list of taken names
    @return a unique name (str) The name will be based on base_name with a number appended to it
    '''
    unique_name = base_name
    number = 0
    while unique_name in list_of_current_names:
        number = number + 1
        unique_name = '%s_%d' %(base_name, number)
    return unique_name
