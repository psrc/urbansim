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

from opus_core.variables.variable import Variable
from numpy import zeros, logical_and

class total_home_based_employment(Variable):
    """
    """
            
    def dependencies(self):
        return ["urbansim_parcel.job.dummy_id",
                "_total_home_based_employment = faz_sector.aggregate(job.building_type==1)", 
               ]

    def compute(self,  dataset_pool):
        faz_sectors = self.get_dataset()
        return faz_sectors.get_attribute("_total_home_based_employment")
