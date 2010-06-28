# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model import Model
from opus_core.model_coordinators.model_system import ModelSystem
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger

class IterativeMetaModel(Model):
    """ This meta model iterates over a set of given models and stops when a given condition is fulfilled.
    """
    model_name = "Iterative Meta Model"

    def __init__(self, models, configuration, datasets_to_preload=None):
        """ 'models' is a list of strings determining the models to be run. 
            'configuration' is a dictionary based configuration used for ModelSystem. 
            Its entry 'models_configuration' must contain the given 'models'. 
            'datasets_to_preload' is a list of dataset names that should
            be pre-loaded for the use of the 'models'. If it is None, all datasets
            in configuration['datasets_to_preload'] are loaded prior to each run.
            Setting this entry can speed the run-time, since all pre-loaded datasets
            are also cached after each iteration. 
        """
        self.config = Resources(configuration)
        self.config['models'] = models
        if datasets_to_preload is not None:
            new_datasets_to_preload = {}
            for dataset in datasets_to_preload:
                new_datasets_to_preload[dataset] = self.config['datasets_to_preload'].get(dataset, {})
            self.config['datasets_to_preload'] = new_datasets_to_preload
        self.model_system = ModelSystem()

    def run(self, year, condition=None, max_iter=10):
        """
        'year' is the current year of the simulation.
        'condition' is an expression. It should be defined on the dataset 'alldata' and thus result in
        exactly one value, usually False or True. The method iterates over the given models until 
        the condition results in True. 
        'max_iter' gives the maximum number of iterations to run, if 'condition' is not fulfilled.
        If it is None, there is no limit and thus, the condition must be fulfilled in order to terminate.
        If 'condition' is None, the set of models is run only once.
        """
        self.config['years'] = (year, year)
        if condition is None:
            return self.model_system.run_in_same_process(self.config)
        dataset_pool = SessionConfiguration().get_dataset_pool()
        alldata = dataset_pool.get_dataset('alldata')
        condition_value = alldata.compute_variables(condition, dataset_pool=dataset_pool)
        result = None
        iter = 1
        while not condition_value:
            result = self.model_system.run_in_same_process(self.config)
            if max_iter is None or iter > max_iter:
                break
            iter = iter + 1
            # force to recompute the condition
            alldata.delete_computed_attributes()
            condition_value = alldata.compute_variables(condition, 
                                                        dataset_pool=SessionConfiguration().get_dataset_pool())
        if not condition_value:
            logger.log_status('%s did not converge. Maximum number of iterations (%s) reached.' % (self.model_name, max_iter))
        else:
            logger.log_status('%s converged in %s iterations.' % (self.model_name, iter-1))  
        return result
    
