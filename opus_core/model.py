# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import sys
import time

from numpy import array, where, arange, zeros
from inspect import getmembers, isroutine
from opus_core.model_component import ModelComponent
from opus_core.logger import logger
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.session_configuration import SessionConfiguration
from opus_core.status_for_gui import StatusForGui

class Model(ModelComponent):
    """The base class for all Opus models.
    Uses logger to automatically start a logger block when the model
    starts running, and close the logger block when the model ends.
    Records the duration of the model run.
    Provides a hook for additional processing of the model duration.
    Each model can define it's model_name.
    """

    def __new__(cls, *args, **kwargs):
        """Setup to automatically log the running time of the run and
        estimate methods."""

        # Set default model name
        model_name = None
        an_instance = ModelComponent.__new__(cls, *args, **kwargs)

        if 'run' in map(lambda (name, obj): name, getmembers(an_instance, isroutine)):
            run_method = an_instance.run
            def logged_run_method (*req_args, **opt_args):
                logger.start_block("Running %s" % an_instance.full_name(), tags=["model", "model-run"],
                                                                        verbosity_level=1)
                try:
                    results = run_method(*req_args, **opt_args)
                finally:
                    logger.end_block()
                return results
            an_instance.run = logged_run_method

        if 'estimate' in map(lambda (name, obj): name, getmembers(an_instance, isroutine)):
            estimate_method = an_instance.estimate
            def logged_estimate_method (*req_args, **opt_args):
                logger.start_block("Estimating %s" % an_instance.full_name(), tags=["model", "model-estimate"],
                                                                        verbosity_level=1)
                try:
                    results = estimate_method(*req_args, **opt_args)
                finally:
                    logger.end_block()
                return results
            an_instance.estimate = logged_estimate_method

        # set defaults for status attributes
        an_instance.status_for_gui = StatusForGui(model=an_instance)
        an_instance.status_for_gui.initialize_pieces(1)
        return an_instance
                                           
    def name(self):
        """return the simple name of this model, either its name if it has one, or else the class name"""
        if hasattr(self, 'model_name') and (self.model_name is not None):
            return self.model_name
        else:
            return self.__class__.__name__

    def full_name(self):
        """return the full name of this model (including which module it is from)"""
        if hasattr(self, 'model_name') and (self.model_name is not None):
            return '%s (from %s)' % (self.model_name, self.__module__)
        else:
            return '%s.%s' % (self.__module__, self.__class__.__name__)

    def do_check(self, condition_str, values):
        """Print a warning message indicating the number of values in values
        that do not meet the condition specified in condition_str.
        """
        def condition(x):
            return eval(condition_str)
        count = where(array(map(lambda x: not(condition(x)), values)) > 0)[0].size
        if (count > 0):
            logger.log_warning("Model %s fails %d times on check: %s" % (self.__class__.__module__, count,  condition_str),
                                tags=["model", "model-check"])

    def map_agents_to_submodels(self, submodels, submodel_string, agent_set, agents_index,
                                 dataset_pool=None, resources=None):
        """ Creates a class attribute self.observations_mapping which is a dictionary
        where each entry corresponds to one submodel. It contains indices
        of agents (within agents_index) that belong to that submodel.
        Additionally, self.observations_mapping has an entry 'index' which contains agents_index, and an entry
        'mapped_index' which contains only indices of agents_index that are included in any of the submodel entries of 
        observations_mapping. Thus, missing entries of 'index' are agents that do not belong to any submodel. 
        'submodels' is a list of submodels to be considered.
        'submodel_string' specifies the name of attribute/variable that distinguishes submodels.
        'resources' are passed to the computation of variable 'submodel_string'.
        """
        self.observations_mapping = {} # maps to which submodel each observation belongs to
        nsubmodels = len(submodels)
        if (nsubmodels > 1) or ((nsubmodels == 1) and (submodels[0] <> -2)):
            try:
                agent_set.compute_variables(submodel_string, dataset_pool=dataset_pool, resources=resources)
            except:
                pass
            if (nsubmodels == 1) and ((submodel_string is None) or (submodel_string not in agent_set.get_known_attribute_names())):
                self.observations_mapping[submodels[0]] = arange(agents_index.size)
            else:
                for submodel in submodels: #mapping agents to submodels
                    w = where(agent_set.get_attribute_by_index(submodel_string,
                                                               agents_index) == submodel)[0]
                    self.observations_mapping[submodel] = w
        else: # no submodel distinction
            self.observations_mapping[-2] = arange(agents_index.size)
        
        mapped = zeros(agents_index.size, dtype='bool8')
        for submodel, index in self.observations_mapping.iteritems():
            mapped[index] = True
        self.observations_mapping["index"] = agents_index
        self.observations_mapping["mapped_index"] = where(mapped)[0]

    def get_all_data(self, submodel=-2):
        """Model must have a property 'data' which is a dictionary that has for each submodel
        some data. It returns data for the given submodel. Meant to be used for analyzing estimation data."""
        if submodel in self.data.keys():
            return self.data[submodel]
        logger.log_warning("No available data for submodel %s." % submodel)
        return None

    def get_data(self, coefficient, submodel=-2, is3d = False):
        """Model must have properties 'data' and 'coefficient_names' which are dictionaries that have for each submodel
        some data and coefficient names respectively. data is a 2D array where columns correspond to
        the coefficient names. If is3d is True, data is 3D array where the second dimension
        correspond to coefficient names. It returns data for the given submodel and coefficient name.
        Meant to be used for data exploration (see GenericDataExplorer)."""
        data = self.get_all_data(submodel)
        names = self.get_coefficient_names(submodel)
        if (names is not None) and (coefficient in names) and (data is not None):
            if is3d:
                return data[:, :, names == coefficient].reshape((data.shape[0], data.shape[1]))
            return data[:, names == coefficient].reshape(data.shape[0])
        logger.log_warning("No coefficient %s exist for submodel %s." % (coefficient, submodel))
        return None

    def get_coefficient_names(self, submodel=-2):
        """ Model must have a property 'coefficient_names' which is a dictionary that has for each submodel
        used coefficient names. It returns coefficient names for the given submodel."""
        if submodel in self.coefficient_names.keys():
            return self.coefficient_names[submodel]
        return None

    def create_dataset_pool(self, dataset_pool, pool_packages=['opus_core']):
        if dataset_pool is None:
            try:
                return SessionConfiguration().get_dataset_pool()
            except:
                return DatasetPool(pool_packages)
        return dataset_pool

    def set_model_system_status_parameters(self, *args, **kwargs):
        self.status_for_gui.set_model_system_parameters(*args, **kwargs)
        
    def get_status_for_gui(self):
        return self.status_for_gui

    def increment_current_status_piece(self):
        self.get_status_for_gui()._increment_current_piece()
        
    def write_status_for_gui(self):
        self.get_status_for_gui().write_status_for_gui()
        
    def _get_status_total_pieces(self):
        return 1
    
    def _get_status_current_piece(self):
        return 0
        
    def _get_status_piece_description(self):
        return ""
    
def get_specification_for_estimation(specification_dict=None, specification_storage=None,
                                        specification_table = None):
    from opus_core.equation_specification import EquationSpecification
    if specification_dict is not None:
        return EquationSpecification(specification_dict=specification_dict)
    (specification, dummy) = prepare_specification_and_coefficients(specification_storage, specification_table)
    return specification

def prepare_specification_and_coefficients(specification_storage=None, specification_table=None, coefficients_storage=None,
                         coefficients_table=None, sample_coefficients=False, cache_storage=None, **kwargs):
    """ Load specification and coefficients from given tables in given storages.
    If 'sample_coefficients' is True, coefficients are sampled from given distribution. In such a case,
    either an argument 'distribution' should be given (equal either 'normal' or 'uniform'), 
    or argument distribution_dictionary should be given containing details about sampling specific coefficients
    (see docstring for method sample_values in opus_core/coefficients.py).
    If coefficients are sampled, the new values are flushed into cache.
    """
    from opus_core.equation_specification import EquationSpecification
    from opus_core.coefficients import Coefficients
    specification = None
    if specification_storage is not None and specification_table is not None:
        specification = EquationSpecification(in_storage=specification_storage)
        specification.load(in_table_name=specification_table)
    coefficients = None
    if (coefficients_storage is not None) and (coefficients_table is not None):
        coefficients = Coefficients(in_storage=coefficients_storage)
        coefficients.load(in_table_name=coefficients_table)
        if sample_coefficients:
            coefficients = coefficients.sample_values(**kwargs)
            coefficients.flush_coefficients(coefficients_table, cache_storage)

    return (specification, coefficients)
    
from opus_core.tests import opus_unittest
import re

class ModelTests(opus_unittest.OpusTestCase):
    def test_name(self):
        t1=TestModel1()
        self.assertEqual(re.search('Test model 1', t1.full_name()) is not None, 1)
        t2 = TestModel2()
        self.assertEqual(re.search('Test model 2', t2.full_name()) is not None, 1)
        t3 = TestModel3()
        self.assertEqual(re.search('TestModel3', t3.full_name()) is not None, 1)

    def test_method_calling_method(self):
        t1=TestModel1()
        t2=TestModel2()
        t2.run()
        t1.run()
        t1.estimate()

class TestModel1(Model):
    model_name = "Test model 1"
    def run(self):
        logger.log_status('in TestModel1.run()')
        t = TestModel2()
        t.run()

    def estimate(self):
        logger.log_status("in estimate()")

    def f(self):
        logger.log_status('in f()')

class TestModel2(Model):
    model_name = "Test model 2"
    def run(self):
        logger.log_status("In TestModel2.run()")
        self.g()

    def g(self):
        logger.log_status('in g()')

class TestModel3(Model):
    # has default name
    def run(self):
        logger.log_status("In TestModel3.run()")
        self.h()

    def h(self):
        logger.log_status('in h()')

if __name__ == '__main__':
    opus_unittest.main()

