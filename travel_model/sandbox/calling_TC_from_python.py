# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import win32com.client as w32c

tc = w32c.Dispatch("TransCAD.AutomationServer")
#display a sample map
tc.Function("MinimizeWindow", "Frame|")
tc.Function("SetMapUnits", "Miles")
tc.Function("SetSearchPath", "tutorial\\")
tc.Function("OpenMap", r"gisdk\samples\activex\bmp_svr.map", None)
tc.Function("SetWindowSizePixels", None, 340, 270)
tc.Function("SetLayer", "Cities & Towns")

#call semcog travel model
tc.RunMacro(r"C:\projects\semcog\T48Core\semcog27Apr2006.rsc")