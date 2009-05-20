# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import SIGNAL, QObject
from PyQt4 import QtGui
from opus_gui.util.icon_library import IconLibrary

def create_qt_action(icon_name, text, callback, parent_qt_object):
    '''
    Convenience method to create actions.
    @param icon_name (str) name of icon to use (no Icon is used of the value is None)
    @param text (str) action label
    @param callback (function) callback function to call when triggered (no parameters)
    @param parent_qt_object (QObject) parent object of action
    @return: the created action (QAction)
    '''
    if icon_name is None:
        action = QtGui.QAction(text, parent_qt_object)
    else:
        action = QtGui.QAction(IconLibrary.icon(icon_name), text, parent_qt_object)
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

def dictionary_to_menu(source_dict, callback, display_func = None, parent_widget = None):
    '''
    Converts a dictionary into a hierarchical menu.
    @param dictionary The dictionary to convert.
    @param callback is called with the object as an argument when a menu item is selected.
    @param display_func An optionally called to display the objects (defaults to str()).
    Example:
     {'one': 'Fish',
      'two': ['orange', 'apple'],
      'three': {'four': 'guppy', 'five': 'guppy'}
     }
    generates a menu with three items in the top level ('one', 'two', 'three')
    'one' contains one item; 'fish'
    'two' contains two items; 'orange' and 'apple'
    'three' contains two submenus; 'four' and 'five'. Both submenus has one item 'guppy'
    '''
    top_menu = QtGui.QMenu(parent_widget)
    if not display_func:
        display_func = str
    for key, items in source_dict.items():
        sub_menu = QtGui.QMenu(key, parent_widget)
        if isinstance(items, dict):
            dict_menu = dictionary_to_menu(items, callback, parent_widget)
            sub_menu.addMenu(dict_menu)
        else:
            for item in list(items): # makes sure single items are iterable
                item_cb = lambda x = item: callback(x)
                action = create_qt_action(None, display_func(item), item_cb, parent_widget)
                sub_menu.addAction(action)
        top_menu.addMenu(sub_menu)
    return top_menu

def hide_widget_on_value_change(widget_to_hide, value_holding_widget,
                               signal = 'textChanged(const QString &)',
                               hide_method = None):
    ''' Hide a widget whenever the value of another widget is changed.
    This method is useful to automatically hide warning labels about erroroneus user input when the
    user starts to correct the input.
    @param widget_to_hide The widget that should be hidden on value change
    @param value_holding_widget The widget to listen for a signal on
    @param signal (default textChanged) the signal to listen for
    @param hide_method the method to call when the signal is recieved (if this argument is omitted,
    a method that consumes all arguments and calls widget_to_hide.setVisible(False)'''
    if hide_method is None:
        def constructed_hide_method(widget = widget_to_hide, *args, **kwargs):
            widget.setVisible(False)
        hide_method = constructed_hide_method
    QtGui.QWidget.connect(value_holding_widget, SIGNAL(signal), hide_method)


