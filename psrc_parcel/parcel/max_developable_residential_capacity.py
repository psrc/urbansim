# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, maximum

class max_developable_residential_capacity(Variable):
    """ Maximum residential capacity (in units) over all generic land use types and units_per_acre 
        allowed by development constraints. 
    """

    def dependencies(self):
        return ["development_constraint.constraint_type"]

    def compute(self,  dataset_pool):
        parcels = dataset_pool.get_dataset("parcel")
        constraints = dataset_pool.get_dataset("development_constraint") 
        parcels.get_development_constraints(constraints, dataset_pool, consider_constraints_as_rules=True)
        result = zeros(parcels.size())
        # iterate over GLU types
        for glu in list(parcels.development_constraints.keys()):
            if  glu == 'index':
                continue
            res_constraints = parcels.development_constraints[glu]['units_per_acre'][:, 1] /43560.0 * parcels['parcel_sqft'] # median of building sqft per unit
            result = maximum(result, res_constraints)
        return result
