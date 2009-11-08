#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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