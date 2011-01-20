# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim_parcel.datasets.development_project_proposal_dataset import create_from_parcel_and_development_template

class max_capacity_using_templates_for_glu_DDD(Variable):
    
    def __init__(self, generic_land_use_type):
        Variable.__init__(self)
        self.glu = generic_land_use_type
        
    def compute(self,  dataset_pool):
        parcels = self.get_dataset()
        templates = dataset_pool.get_dataset('development_template')
        template_components = dataset_pool.get_dataset('development_template_component')
        proposals = create_from_parcel_and_development_template(
                                    parcels, templates, 
                                    filter_attribute="has_vacant_land=urbansim_parcel.parcel.vacant_land_area > 0",
                                    proposed_units_variable="psrc_parcel.development_project_proposal.units_proposed_plus_minimum_1DU_per_legal_lot_yield",
                                    dataset_pool=dataset_pool, resources=None)
        dataset_pool.replace_dataset('development_project_proposal', proposals)
        self.add_and_solve_dependencies([
        "_max_capacity = parcel.aggregate(urbansim_parcel.development_project_proposal.land_area_taken * (development_project_proposal.disaggregate(land_use_type.generic_land_use_type_id, intermediates=[development_template])==%s), function=maximum)" % self.glu
                ])
        return parcels["_max_capacity"]
    