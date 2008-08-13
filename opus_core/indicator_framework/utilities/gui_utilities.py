#
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

def display_message_dialog(message): 
    try:
        import wx
    except: 
        return
    try: 
        try:
            dlg = wx.MessageDialog(None,
                message=message,
                style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        except wx._core.PyNoAppError:
            #don't want to build an app unless its necessary
            app = wx.App() 
            display_message_dialog(message)
    except: pass