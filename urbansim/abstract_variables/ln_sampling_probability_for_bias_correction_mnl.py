#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.variables.variable_name import VariableName
from opus_core.variables.variable import Variable

class ln_sampling_probability_for_bias_correction_mnl(Variable):
    """Abstract variable to be used for correcting for sampling bias when sampling alternatives.
    It is assumed to be an interaction variable. The init function gets the name of the attribute that is used 
    for weighting alternatives in the model. It doesn't need to be normalized, that is done within the function.
    """
    def __init__(self, weights_attribute):
        self.weights_attribute = weights_attribute
        Variable.__init__(self)
        
    def dependencies_to_add(self, dataset_name, package="urbansim"):
        """Will be added to the dependencies from the compute method, because before that we don't 
        know the dataset name."""
        self.weights_attribute = VariableName("%s.%s.%s" % (package, dataset_name, self.weights_attribute))
        return [self.weights_attribute.get_expression(),
                "_normalized_weights = %s/float(sum(%s))" % (self.weights_attribute.get_expression(), self.weights_attribute.get_expression()),
                "_log_weights = ln(%s._normalized_weights)" % self.weights_attribute.get_dataset_name(),
                "_log_1_minus_weights = ln(1 - %s._normalized_weights)" % self.weights_attribute.get_dataset_name()]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset() # interaction dataset
        self.add_and_solve_dependencies(self.dependencies_to_add(ds.get_dataset(2).get_dataset_name()), dataset_pool)
        log_1_minus_weights = ds.get_dataset(2).get_attribute("_log_1_minus_weights")
        result = log_1_minus_weights.sum() - ds.get_attribute("_log_1_minus_weights").sum(axis=1).reshape((ds.get_reduced_n(),1)) - \
               ds.get_attribute("_log_weights") + ds.get_attribute("_log_weights").sum(axis=1).reshape((ds.get_reduced_n(),1))
        return result - result.max() # shift the values to zero