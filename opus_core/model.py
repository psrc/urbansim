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

import sys
import time

from numpy import array, where, arange
from inspect import getmembers, isroutine
from opus_core.model_component import ModelComponent
from opus_core.logger import logger
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.session_configuration import SessionConfiguration

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
                logger.start_block("Running %s" % an_instance.name(), tags=["model", "model-run"],
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
                logger.start_block("Estimating %s" % an_instance.name(), tags=["model", "model-estimate"],
                                                                        verbosity_level=1)
                try:
                    results = estimate_method(*req_args, **opt_args)
                finally:
                    logger.end_block()
                return results
            an_instance.estimate = logged_estimate_method

        return an_instance

    def name(self):
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
        self.observations_mapping["index"] = agents_index

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
        Meant to be used for analyzing estimation data."""
        data = self.get_all_data(submodel)
        names = self.get_coefficient_names(submodel)
        if (names is not None) and (coefficient in names) and (data is not None):
            if is3d:
                return data[:, names == coefficient, :].reshape((data.shape[0], data.shape[2]))
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

from opus_core.tests import opus_unittest
import re

class ModelTests(opus_unittest.OpusTestCase):
    def test_name(self):
        t1=TestModel1()
        self.assertEqual(re.search('Test model 1', t1.name()) is not None, 1)
        t2 = TestModel2()
        self.assertEqual(re.search('Test model 2', t2.name()) is not None, 1)
        t3 = TestModel3()
        self.assertEqual(re.search('TestModel3', t3.name()) is not None, 1)

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

