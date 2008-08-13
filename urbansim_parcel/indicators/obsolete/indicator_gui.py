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

# open a traits-based GUI for editing PSRC indicator requests

from opus_core.indicator_framework.traits.traits_indicator_handler \
    import TraitsIndicatorHandler

handler = TraitsIndicatorHandler()
handler.open_editor(package_order = ['urbansim_parcel', 'urbansim', 'opus_core'])

