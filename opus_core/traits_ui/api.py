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

# Backward compatibility hack for enthought traits ui.  In the current version
# of the enthought code in their stable releases, importing the classes for 
# the UI is from enthought.traits.ui.api, but in the Enthought Python that we
# recommend that our users download, this is from enthougth.traits.api.  We don't 
# want to insist that people get the newer Python right now and stop using the 
# Python Enthought edition, hence this hack.
#
# When we stop using the old Enthought 2.4.3 Python we can get rid of this.  Each
# plance in the code where it is used has a commented-out new style import also.


try:
    from enthought.traits.ui.api import *
except:
    from enthougth.traits.api import *
