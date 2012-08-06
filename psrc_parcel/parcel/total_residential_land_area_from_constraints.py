# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.functions import safe_array_divide
from numpy import zeros, maximum, minimum, where

class total_residential_land_area_from_constraints(Variable):
    """ Total residential land area  allowed by development constraints. 
    """
    _return_type='int32'
    def dependencies(self):
        return ["development_constraint.constraint_type", "psrc_parcel.parcel.residential_units", "parcel.parcel_sqft"]

    def compute(self,  dataset_pool):
        parcels = dataset_pool.get_dataset("parcel")
        constraints = dataset_pool.get_dataset("development_constraint") 
        parcels.get_development_constraints(constraints, dataset_pool, consider_constraints_as_rules=True)
        result = zeros(parcels.size())
        # iterate over GLU types
        for glu in parcels.development_constraints.keys():
            if  glu == 'index':
                continue
            res_constraints = minimum(safe_array_divide(43560.0, parcels.development_constraints[glu]['units_per_acre'][:, 1])*parcels["residential_units"], parcels['parcel_sqft'])
            result = maximum(result, res_constraints)
        equal_zero = where(result <= 0)[0]
        result[equal_zero] = safe_array_divide(parcels['parcel_sqft'][equal_zero], parcels["residential_units"][equal_zero])
        return result

