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


from enthought.traits import HasTraits, Bool
from enthought.traits.ui import View, Handler


class TC_Handler(Handler):

    def setattr(self, info, object, name, value):
        Handler.setattr(self, info, object, name, value)
        info.object._updated = True


    def object__updated_changed(self, info):
        if info.initialized:
            info.ui.title += "*"


class TestClass(HasTraits):
    b1 = Bool
    b2 = Bool
    b3 = Bool
    _updated = Bool(False)


view1 = View('b1', 'b2', 'b3', 
             title="Alter Title on Update", 
             handler=TC_Handler())

tc = TestClass()
tc.configure_traits(view=view1)
