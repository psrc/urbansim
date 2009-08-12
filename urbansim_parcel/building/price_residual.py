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

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class price_residual(abstract_iv_residual):
    """"""
    p = "urbansim_parcel.building.price_per_unit"
    iv = "urbansim_parcel.building.avg_price_per_unit_in_zone"
    filter = "urbansim_parcel.building.building_id>0"

