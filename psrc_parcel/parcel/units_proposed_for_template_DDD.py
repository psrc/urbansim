# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, logical_and, logical_or, logical_not

class units_proposed_for_template_DDD(Variable):
    """Total units (as real numbers) proposed (residential units, and/or non residential sqft) 
    for this template,
    depending on whether the proposed projects will be prorated or not, part or all of the
    units will be available.
    """
    _return_type = "int32"
    mol = 0.1
    ACRE_TO_SQFT = 43560.00
    
    def __init__(self, template_id):
        Variable.__init__(self)
        self.template_id = template_id
        
    def dependencies(self):
        return ["urbansim_parcel.parcel.vacant_land_area"]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        templates = dataset_pool.get_dataset('development_template')
        this_template = templates.get_data_element_by_id(self.template_id, all_attributes=True)
        self.add_and_solve_dependencies([])
        
        vacant_land_area = ds.get_attribute("vacant_land_area")
        land_area_taken = vacant_land_area.astype("int32").copy()
        w_min = where(land_area_taken<this_template.land_sqft_min)
        land_area_taken[w_min] = 0 
        w_max = where(land_area_taken > this_template.land_sqft_max * (1+self.mol) )
        land_area_taken[w_max] = int(this_template.land_sqft_max)
        
        usable_ratio = 1 - this_template.percent_land_overhead / 100.0
        density_convertor = 1.0
        if this_template.density_type == 'units_per_acre':
            density_convertor = 1.0 / self.ACRE_TO_SQFT
        result = land_area_taken * usable_ratio * this_template.density * density_convertor
        min_rural = logical_and(result <= 0.5, logical_and(result > 0, logical_and(ds['parcel_sqft'] > 9999, 
                                                            logical_not(ds['is_inside_urban_growth_boundary']))))
        min_urban = logical_and(result <= 0.5, logical_and(result > 0, logical_and(ds['parcel_sqft'] > 3499, 
                                                            ds['is_inside_urban_growth_boundary'])))
        return result.astype("int32") + logical_and(this_template.density_type == 'far', logical_or(min_rural, min_urban))

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

