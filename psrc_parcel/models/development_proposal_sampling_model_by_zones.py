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

from numpy import arange, zeros, logical_and, where, logical_not
from opus_core.logger import logger
from urbansim_parcel.models.development_project_proposal_sampling_model import DevelopmentProjectProposalSamplingModel
from opus_core.datasets.dataset import DatasetSubset

class DevelopmentProposalSamplingModelByZones(DevelopmentProjectProposalSamplingModel):
        
    def run(self, zones, *args, **kwargs):

        zones.compute_variables(["occupied_residential_units = urbansim_parcel.zone.number_of_households",
                                 "existing_residential_units = zone.aggregate(building.residential_units, [parcel])"],
                                dataset_pool=self.dataset_pool)
        occupied_residential_units = zones.get_attribute("occupied_residential_units")
        exisiting_residential_units = zones.get_attribute("existing_residential_units")
        zone_ids = zones.get_id_attribute()

        zone_index = 0
        for zone_id in zone_ids[0:10]:
            self.zone = zone_id
            self.existing_to_occupied_ratio =  exisiting_residential_units[zone_index] / float(occupied_residential_units[zone_index])
            self.proposal_set.compute_variables("zone_id = development_project_proposal.disaggregate(parcel.zone_id)", 
                                                dataset_pool=self.dataset_pool)
            status = self.proposal_set.get_attribute("status_id")
            where_zone = self.proposal_set.get_attribute("zone_id") == zone_id
            idx_zone = where(where_zone)[0]
            idx_out_zone_not_active = where(logical_and(status != self.proposal_set.id_active, logical_not(where_zone)))[0]
            status[idx_zone] = self.proposal_set.id_proposed
            status[idx_out_zone_not_active] = self.proposal_set.id_not_available
            self.proposal_set.modify_attribute(name="status_id", data=status)
            #self.proposal_set = DatasetSubset(self.proposal_set, 
            #                                  index = where(self.proposal_set.get_attribute("zone_id") == zone_id)[0])
            logger.log_status("DPSM for zone %s" % zone_id)
            DevelopmentProjectProposalSamplingModel.run(self, *args, **kwargs)
            zone_index += 1
        return self.proposal_set

    def check_vacancy_rates(self, target_vacancy):

        for index in arange(target_vacancy.size()):
            ##TODO allow target vacancies to vary across zones/sub region geographies
            #zone_id = target_vacancy.get_attribute_by_index("zone_id", index)
            #if zone_id != self.zone: continue

            type_id = target_vacancy.get_attribute_by_index("generic_building_type_id", index)
            type_name = target_vacancy.get_attribute_by_index("type_name", index)
            unit_name = target_vacancy.get_attribute_by_index("unit_name", index)  #vacancy by type, could be residential, non-residential, or by building_type
            target = target_vacancy.get_attribute_by_index("target_vacancy_rate", index)
            buildings = self.dataset_pool.get_dataset("building")
            is_matched_type = buildings.get_attribute("generic_building_type_id") == type_id
            is_in_right_zone = buildings.get_attribute("zone_id") == self.zone
            existing_units = buildings.get_attribute(unit_name)[is_matched_type*is_in_right_zone]
            occupied_units = buildings.get_attribute("occupied_%s" % unit_name)[is_matched_type*is_in_right_zone]

            self.existing_units[type_id] = existing_units.astype("float32").sum()
            if unit_name == "residential_units":
                self.occupied_units[type_id] = int(self.existing_units[type_id]/self.existing_to_occupied_ratio)
            else:
                self.occupied_units[type_id] = occupied_units.astype("float32").sum()
            self.proposed_units[type_id] = 0
            self.demolished_units[type_id] = 0
            vr = (self.existing_units[type_id] - self.occupied_units[type_id]) / float(self.existing_units[type_id])
            if vr < target:
                self.accepting_proposals[type_id] = True
            else:
                self.accepting_proposals[type_id] = False
