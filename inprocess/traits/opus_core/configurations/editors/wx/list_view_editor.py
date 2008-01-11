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

# Portions of the following are covered by the following license:
#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------

import wx

from enthought.traits.api import Dict, List, Any, Bool, Undefined

# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from opus_core.traits_ui.api import View, Group, Item

from enthought.traits.ui.wx.editor import EditorWithList
from enthought.traits.ui.wx.constants import ReadonlyColor
from enthought.traits.ui.wx.text_editor import SimpleEditor as TextEditor
from enthought.traits.ui.wx.editor_factory import EditorWithListFactory

from opus_core.wx.force_redraw import ForceRedraw


class ToolkitEditorFactory(EditorWithListFactory):
    def __init__(self, view, *args, **traits):
        self.add_trait('traits_view', Any(view))
        EditorWithListFactory.__init__(self, *args, **traits)
        
    def simple_editor(self, ui, object, name, description, parent):
        return SimpleEditor(parent, factory=self, ui=ui, object=object, 
            name=name, description=description)
    
    def custom_editor(self, ui, object, name, description, parent):
        return SimpleEditor(parent, factory=self, ui=ui, object=object, 
            name=name, description=description)
    
    def text_editor(self, ui, object, name, description, parent):
        return TextEditor(parent, factory=self, ui=ui, object=object, 
            name=name, description=description)
    
    def readonly_editor(self, ui, object, name, description, parent):
        return SimpleEditor(parent, factory=self, ui=ui, object=object, 
            name=name, description=description)
            
                              
class SimpleEditor(EditorWithList):
    my_controls = List
    
    def init(self, parent):
        self.control = wx.ScrolledWindow(parent)
        self.control.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.control.SetScrollRate(16,16)

        self._create_control()
        
        self.set_tooltip()
        
        super(SimpleEditor, self).init(parent)
        
    def list_updated(self, values):
        self.value = values
        self._rebuild_editor()
        
    def update_editor(self):
        # This stuff is taken care of by the subpanel views.
        pass
    
    def _rebuild_editor(self):
        self.control.DestroyChildren()
        self._create_control()
        self.update_editor()
        
    def _create_control(self):
        for has_traits_item in self.value:
            self._add_has_traits_item_to_control(has_traits_item)
            
        ### Stupid hack to force a redraw in Windows.
        ForceRedraw().force_redraw(self.control)    
    
    def _add_has_traits_item_to_control(self, has_traits_item):
        ui = has_traits_item.edit_traits(view=self.factory.traits_view, 
            parent=self.control, kind='subpanel')
        self.control.GetSizer().Add(ui.control)

        # Chain our undo history to the new user interface if it does not have
        # its own:
        if ui.history is Undefined:
            ui.history = self.control.history
        self.my_controls.append((has_traits_item, ui.control))