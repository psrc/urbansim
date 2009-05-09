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

# Constants for checking returned answers
UNKNOWN_ANSWER = -1
NO = 0
YES = 1
CANCEL = 2

from PyQt4.QtGui import QMessageBox
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance

def _action_before_continue(question, buttons, parent_widget):
    ''' base for dialogs that ask users to close with dirty data '''
    if parent_widget is None:
        parent_widget = get_mainwindow_instance()
    ok_answers = [QMessageBox.Apply, QMessageBox.Save]
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
