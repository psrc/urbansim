# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# Constants for checking returned answers
UNKNOWN_ANSWER = -1
NO = 0
YES = 1
CANCEL = 2

from PyQt5.QtWidgets import QMessageBox
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance

def _action_before_continue(question, buttons, parent_widget):
    ''' base for dialogs that ask users to close with dirty data '''
    if parent_widget is None:
        parent_widget = get_mainwindow_instance()
    ok_answers = [QMessageBox.Apply, QMessageBox.Save, QMessageBox.Yes]
    answer = QMessageBox.question(parent_widget, "Warning", question, *buttons)
    if answer in ok_answers:
        return YES
    elif answer == QMessageBox.Discard:
        return NO
    elif answer == QMessageBox.Cancel:
        return CANCEL
    return UNKNOWN_ANSWER

def save_before_close(question, parent_widget = None):
    '''
    Ask the users if they want to save, discard or cancel before continuing.
    @param question the question to ask the user
    @return the answer (common_dialogs.YES|NO|CANCEL)
    '''
    buttons = (QMessageBox.Discard, QMessageBox.Save, QMessageBox.Cancel)
    return _action_before_continue(question, buttons, parent_widget)

def apply_before_close(question, parent_widget = None):
    '''
    Ask the users if they want to apply, discard or cancel before continuing.
    @param question the question to ask the user
    @return the answer (common_dialogs.YES|NO|CANCEL)
    '''
    buttons = (QMessageBox.Discard, QMessageBox.Apply, QMessageBox.Cancel)
    return _action_before_continue(question, buttons, parent_widget)

def yes_or_cancel(question, parent_widget = None):
    '''
    Ask the users if it is OK to continue, or cancel the action.
    @param question the question to ask the user
    @return the answer (common_dialogs.YES|CANCEL)
    '''
    buttons = (QMessageBox.Yes, QMessageBox.Cancel)
    return _action_before_continue(question, buttons, parent_widget)

def user_is_sure(question, parent_widget = None):
    buttons = (QMessageBox.Yes, QMessageBox.No)
    return _action_before_continue(question, buttons, parent_widget) == YES
