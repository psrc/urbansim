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

from enthought.traits.api import Button, Constant, HasTraits, Trait
# later update the ui import to:   from enthought.traits.ui.api import Handler, Item, Group, View
from enthought.traits.api import Handler, Item, Group, View
from enthought.traits.ui.menu import Action, Menu, MenuBar, CloseAction, HelpAction, NoButtons
import wx
import cPickle as pickle


class OpusControlCenter(HasTraits):
    """Control center for the Opus Graphical User Interface"""
    # currently no functionality in the control center itself ...
    pass


class OpusControlCenterHandler(Handler):
    """Handler for the Opus Graphical User Interface Control Center"""
    # *** Traits ***
    # last_window_location is the upper-left corner of the last editing window that
    # was opened.  We use this to avoid opening windows on top of each other, and instead
    # keep offsetting the new location a bit.  (After a while reset this to start again
    # at the original position to avoid going off the screen.)
    last_window_location = Trait(wx.Point)
    # constants
    wildcard_string = Constant("Opus files (*.opus)|*.opus|All files (*.*)|*.*")
    # buttons
    open_configuration_editor = Button("Open configuration editor")

    # method to handle the 'open' button action
    def handler_open_configuration_editor_changed(self,info):
        self.do_open(info)
        
    # method to handle the 'open' menu item (also called by the handler for the open button)
    def do_open(self,info):
        dlg = wx.FileDialog(None,
                            message="Open ...",
                           # defaultFile=self.default_config_file_name,
                            style=wx.OPEN,
                            wildcard=self.wildcard_string)
        if dlg.ShowModal()==wx.ID_OK:
            name = dlg.GetPath()
            try:
                f = open(name,'r')
                (unpickled_config,unpickled_handler) = pickle.load(f)
                f.close()
                # set the pickle file name of the unpickled_handler to the name of the file 
                # just opened, since the file name isn't stored in the pickle file itself.  
                # This doesn't count as making the handler dirty, so also set updated to false.
                unpickled_handler.pickle_file = name
                unpickled_handler.updated = False
                if self.last_window_location is None or self.last_window_location.x>400:
                    self.last_window_location = wx.Point(100,100)
                self.last_window_location = self.last_window_location+wx.Point(30,20)
                unpickled_handler.open_editor(unpickled_config, location=self.last_window_location)
            except pickle.UnpicklingError:
                wx.MessageBox("%s is not a pickled configuration file." % name,
                          style=wx.OK | wx.ICON_EXCLAMATION)
        dlg.Destroy()
        
if __name__ == '__main__':
    model = OpusControlCenter()
    handler = OpusControlCenterHandler()
    OpenAction = Action(name="Open configuration editor", action="do_open")
    file_menu = Menu(OpenAction, CloseAction, name='File')
    help_menu = Menu(HelpAction, name='Help')
    # help strings
    open_help = """Press this button to open a file dialog.  Then use the dialog to select an Opus
        configuration file.  The system will respond by opening a traits editor on the
        configuration file, customized to that kind of configuration.  Each successive editor
        is opened at a slightly offset location from the last, to avoid piling the windows up
        on top of each other (eventually resetting so that they don't go off the screen)."""
    view = View(Group(
                    '10', 
                    Group('20', Item('open_configuration_editor', object='handler', help=open_help), '20', orientation='horizontal', show_labels=False),
                    '10',
                    orientation='vertical'),
                buttons = NoButtons,
                menubar = MenuBar(file_menu, help_menu), 
                title='Opus Control Center',
                x=20,
                y=40)
    model.configure_traits(view=view, handler=handler)
