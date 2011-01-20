# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable_name import VariableName
from opus_core.variables.variable import Variable

class ln_sampling_probability_for_bias_correction_mnl(Variable):
    """Abstract variable to be used for correcting for sampling bias when sampling alternatives.
    It is assumed to be an interaction variable. The init function gets the name of the attribute that is used 
    for weighting alternatives in the model. It doesn't need to be normalized, that is done within the function.
    """
    def __init__(self, weights_attribute):
        self.weights_attribute_name = weights_attribute
        Variable.__init__(self)
        
    def dependencies_to_add(self, dataset_name, package="urbansim"):
        """Will be added to the dependencies from the compute method, because before that we don't 
        know the dataset name."""
        self.weights_attribute = VariableName("%s.%s.%s" % (package, dataset_name, self.weights_attribute_name))
        return [self.weights_attribute.get_expression(),
                "_normalized_weights_%s = %s/float(sum(%s))" % (self.weights_attribute_name, self.weights_attribute.get_expression(), self.weights_attribute.get_expression()),
                "_log_weights_%s = ln(%s._normalized_weights_%s)" % (self.weights_attribute_name, self.weights_attribute.get_dataset_name(), self.weights_attribute_name),
                "_log_1_minus_weights_%s = ln(1 - %s._normalized_weights_%s)" % (self.weights_attribute_name, self.weights_attribute.get_dataset_name(), self.weights_attribute_name)]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset() # interaction dataset
        self.add_and_solve_dependencies(self.dependencies_to_add(ds.get_dataset(2).get_dataset_name()), dataset_pool)
        log_1_minus_weights = ds.get_dataset(2).get_attribute("_log_1_minus_weights_%s" % self.weights_attribute_name)
        result = log_1_minus_weights.sum() - ds.get_attribute("_log_1_minus_weights_%s" % self.weights_attribute_name).sum(axis=1).reshape((ds.get_reduced_n(),1)) - \
               ds.get_attribute("_log_weights_%s" % self.weights_attribute_name) + ds.get_attribute("_log_weights_%s" % self.weights_attribute_name).sum(axis=1).reshape((ds.get_reduced_n(),1))
        return result - result.max() # shift the values to zero