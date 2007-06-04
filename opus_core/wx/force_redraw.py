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

class ForceRedraw(object):
    def force_redraw(self,control):
        """
        Stupid hack to force a redraw on a control and its ancestors. Needed in
        certain situations on Windows machines.
        """
        try:
            x,y = control.GetSize()
            control.SetSize((x, y+1))
            control.SetSize((x,y))
            force_redraw(control.GetParent())
        except:
            pass