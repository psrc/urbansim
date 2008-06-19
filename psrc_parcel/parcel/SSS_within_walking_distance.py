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

from psrc.parcel.SSS_within_walking_distance import SSS_within_walking_distance as PSRC_SSS_within_walking_distance

class SSS_within_walking_distance(PSRC_SSS_within_walking_distance):
    """Sum over c in cell.walking_radius, c.residential_units."""
        
    def dependencies(self):
        return ['grid_id=household.disaggregate(parcel.grid_id, intermediates=[building])',
                'grid_id=job.disaggregate(parcel.grid_id, intermediates=[building])',
                'urbansim.gridcell.' + self.var_name,
                "gridcell.grid_id",
                'parcel.grid_id']
