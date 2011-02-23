# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import logical_and, zeros

class is_size_fit_for_template_DDD(Variable):
    """Whether this development template with its land_sqft min and max is viable for a given parcel.
    """
    _return_type = "bool8"
    
    def __init__(self, template_id):
        Variable.__init__(self)
        self.template_id = template_id
        
    def dependencies(self):
        return ["urbansim_parcel.parcel.vacant_land_area"]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        templates = dataset_pool.get_dataset('development_template')
        this_template = templates.get_data_element_by_id(self.template_id, all_attributes=True)
        results = zeros(ds.size(), dtype=self._return_type)
        results[logical_and(ds.get_attribute("vacant_land_area") >= this_template.land_sqft_min,
                              ds.get_attribute("vacant_land_area") <= this_template.land_sqft_max )] = True
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

