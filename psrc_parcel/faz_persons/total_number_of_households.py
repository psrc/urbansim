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

class total_number_of_households(Variable):
    """
    """
            
    def dependencies(self):
        return ["urbansim_parcel.household.dummy_id",
                "_total_number_of_households = faz_persons.number_of_agents(household)", 
               ]

    def compute(self,  dataset_pool):
        faz_sectors = self.get_dataset()
        return faz_sectors.get_attribute("_total_number_of_households")
