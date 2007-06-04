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

from enthought.traits import HasTraits
# wrap the import of traits.ui in a try/except block.  This allows
# a configuration to be used without the traits UI; however,
# you won't be able to configure it using the interactive editor.
# Subclasses won't need to import enthought.traits.ui to get this
# functionality -- just importing it in the superclass takes care of it.
try:
    import enthought.traits.ui
except:
    pass 

class AbstractConfiguration(HasTraits):
    """AbstractConfiguration is an abstract superclass for Opus configurations of all kinds,
    using the Enthought traits mechanism.  Right now there isn't any functionality 
    here, but some will be added in the future."""
    pass
