# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import array, reshape, concatenate, ones, arange, exp, newaxis, eye
from numpy import size, where, zeros, empty, dot, transpose, repeat
from numpy.linalg import inv

class abstract_iv_residual(Variable):
    """"""
    p = "to_be_specified_in_full_qualified_variable_name" # dependent variable in 1st stage IV regression
    iv = "to_be_specified_in_full_qualified_variable_name" # IV
    filter = "to_be_specified_in_full_qualified_variable_name" #filter deciding which records are included in IV regression

    def dependencies(self):
        return [
                self.p,
                self.iv,
                self.filter
                ]

    def compute(self,  dataset_pool):
        ds = self.get_dataset()
        filter = ds.get_attribute(self._get_alias(self.filter))
        # dependent variable - price
        y = ds.get_attribute_as_column(self._get_alias(self.p))[filter, :]
        # independent variables - in vector
        z = ds.get_attribute_as_column(self._get_alias(self.iv))[filter, :]
        #import pdb; pdb.set_trace()
        z = concatenate( (ones(z.shape), z), axis=-1)

        zt = transpose(z)
        est = dot( dot( inv(dot(zt, z)), zt), y )
        r =  y - dot( z, est )

        results = zeros(ds.size(), dtype=r.dtype)
        results[filter] = r[:, 0]
        return results

    def _get_alias(self, expression):
        return VariableName(expression).get_alias()

# Unit test in urbansim_parce/building/price_residual