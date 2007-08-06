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

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from psrc_parcel.models.household_location_choice_model import HouseholdLocationChoiceModel

class HouseholdLocationChoiceModelByZones(HouseholdLocationChoiceModel):
        
    def run(self, zones, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        zone_ids = zones.get_id_attribute()
        agents_zones = agent_set.get_attribute(zones.get_id_name()[0])
        for zone_id in zone_ids:
            new_index = where(logical_and(cond_array, agents_zones == zone_id))[0]
            self.filter = "building.zone_id == %s" % zone_id
            logger.log_status("HLCM for zone %s" % zone_id)
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
        # set the right parcels
        parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
                                              dataset_pool = self.dataset_pool)
        agent_set.modify_attribute(name="parcel_id", data = parcels)