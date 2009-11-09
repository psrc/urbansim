# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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