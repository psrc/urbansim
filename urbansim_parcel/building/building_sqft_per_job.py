# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class building_sqft_per_job(Variable):
    """ building sqft per job disaggregated from the zonal-building_type averages"""
    
    _return_type = "int32"
    
    def dependencies(self):
        return ["building_sqft_per_job.building_sqft_per_job",
                "urbansim_parcel.building.zone_id",
                "building.building_type_id",
                ]

    def compute(self,  dataset_pool):
        sqft_per_job = dataset_pool.get_dataset("building_sqft_per_job")
        buildings = self.get_dataset()
        zones = buildings.get_attribute("zone_id")
        type_ids = buildings.get_attribute("building_type_id")
        building_sqft_per_job_table = sqft_per_job.get_building_sqft_as_table(zones.max(), type_ids.max())
        return building_sqft_per_job_table[zones, type_ids]

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
