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

from psrc.abstract_variables.abstract_logsum_variable import abstract_logsum_variable
from opus_core.variables.variable import Variable
from numpy import newaxis, concatenate

class max_logsum_hbw_am_from_home_to_work(Variable):
    """max_logsum_hbw_am_from_home_to_work between worker1 & worker2"""
    
    def dependencies(self):
        return [ 
                "psrc_parcel.household_x_building.worker1_logsum_hbw_am_from_home_to_work",
                "psrc_parcel.household_x_building.worker2_logsum_hbw_am_from_home_to_work",
             ]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        data1 = interaction_dataset.get_attribute("worker1_logsum_hbw_am_from_home_to_work")
        data2 = interaction_dataset.get_attribute("worker2_logsum_hbw_am_from_home_to_work")

        return concatenate((data1[...,newaxis], data2[...,newaxis]), axis=2).max(axis=2)