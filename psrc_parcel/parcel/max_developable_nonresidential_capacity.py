# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, maximum

class max_developable_nonresidential_capacity(Variable):
    """ Maximum capacity over all generic land use types and over far 
        allowed by development constraints. 
        The median of building sqft per unit (1553) is used.
    """

    def dependencies(self):
        return ["development_constraint.constraint_type"]

    def compute(self,  dataset_pool):
        parcels = dataset_pool.get_dataset("parcel")
        constraints = dataset_pool.get_dataset("development_constraint") 
        parcels.get_development_constraints(constraints, dataset_pool, consider_constraints_as_rules=True)
        result = zeros(parcels.size())
        # iterate over GLU types
        for glu in parcels.development_constraints.keys():
            if  glu == 'index':
                continue
            result = maximum(result, parcels.development_constraints[glu]['far'][:, 1]*parcels['parcel_sqft'])  #max constraint
        return result
