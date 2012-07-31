# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import re
import os
import sys
import time
import pickle
import subprocess
import numpy as np
from copy import copy
from scipy.optimize import *
from numpy.random import seed
from numpy import array, arange
from opus_core.logger import logger, log_block
from opus_core.simulation_state import SimulationState
from opus_core.configurations.config_calibration import *
from opus_core.store.attribute_cache import AttributeCache
from opus_core.variables.variable_name import VariableName
from opus_core.services.run_server.run_manager import RunManager
from opus_core.session_configuration import SessionConfiguration
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.tools.start_run import StartRunOptionGroup, main as start_run
from opus_core.tools.restart_run import RestartRunOptionGroup, main as restart_run
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

try:
    is_parallelizable = is_parallelizable
    lock = lock
    print HEADER+"-------------- parallel --------------"+ENDC
except NameError:
    is_parallelizable = False
    lock = None
    print HEADER+"-------------- non parallel --------------"+ENDC

class Calibration(object):
    ''' Class to calibrate UrbanSim model coefficients.
    
    '''
    def __init__(self, xml_config, scenario, calib_datasets, target_expression, target_file,
                 subset=None, subset_patterns=None, skip_cache_cleanup=False, log_directory=None):
        """
        - xml_config: xml configuration file, for ex '/home/atschirhar/opus/project_configs/paris_zone.xml'
        - scenario: name of scenario to run for calibration, where models_to_run and simulation years are specified
        - calib_datasets: dictionary specifying dataset names and attributes to be calibrated, e.g.
                  {'establishment_location_choice_model_coefficients': 'estimate'}
        - target_expression: opus expression computing values from prediction to be compared with targets 
        - target_file: name of csv file providing targets 
        - subset: dictionary specifying the dataset to be calibrated,
                  {'etablishment_location_choice_model_coefficients': ['coefficient_name', ['paris_celcm, 'biotech_celcm']]}
          subset and subset_patterns can not be both specified for the same dataset
        - subset_patterns: dictionary specifying the dataset to be calibrated through a regular expression (re) pattern
                  {'etablishment_location_choice_model_coefficients': ['coefficient_name', '*_celcm']} 
          subset and subset_patterns can not be both specified for the same dataset

        """
        self.target_expression = target_expression
        self.target = self.read_target(target_file)

        self.run_manager = None
        self.xml_config = xml_config
        self.scenario = scenario
        self.skip_cache_cleanup = skip_cache_cleanup
        self.run_id, self.cache_directory = self.init_run()
        self.run_ids = [self.run_id]  #allow starting of multiple runs for parallel optimization
        self.log_directory = log_directory
        if self.log_directory is None:
            self.log_directory = self.cache_directory #legacy

        log_file = os.path.join(self.log_directory, "calibration.log")
        logger.enable_file_logging(log_file)

        dict_config = XMLConfiguration(self.xml_config).get_run_configuration(self.scenario)
        ## get parameters from config
        self.base_year = dict_config['base_year']
        self.start_year, self.end_year = dict_config['years']
        self.project_name = dict_config['project_name']
        self.package_order = dict_config['dataset_pool_configuration'].package_order
        

    @log_block("Start Calibration")
    def run(self, optimizer='lbfgsb', results_pickle_prefix="calib", optimizer_kwargs={}):
        ''' Call specifized optimizer to calibrate
        
        Arguments:
            - optimizer: optimization method chosen (fmin_bfgs, simulated anneal etc.)
            - results_pickle_prefix: prefix of the pickle file name that will be saved after the simulation; if None, results is not saved
            
        Returns:
            - the results from the opimizater
            - a pickle dump of the results in the cache_directory, if results_pickle_prefix is specified
        
        '''

        simulation_state = SimulationState()
        simulation_state.set_current_time(self.base_year)
        simulation_state.set_cache_directory(self.cache_directory)
        attribute_cache = AttributeCache()
        dataset_pool = SessionConfiguration(new_instance=True,
                                  package_order=self.package_order,
                                  in_storage=attribute_cache
                                  ).get_dataset_pool()

        calib_datasets = {}
        for dataset_name, calib_attr in calib_datasets.iteritems():
            dataset = dataset_pool.get_dataset(dataset_name, 
                                                    dataset_arguments={'id_name':[]})
            assert subset is None or subset.get(dataset_name, None) is None or \
                   subset_patterns is None or subset_patterns.get(dataset_name, None) is None
            if subset is not None and subset.get(dataset_name, None) is not None:
                subset_attr, subset_cond = subset.get(dataset_name) 
                index = np.in1d(dataset[subset_attr], subset_cond)
            elif subset_patterns is not None and subset_patterns.get(dataset_name, None) is not None:
                subset_attr, subset_pattern = subset_patterns.get(dataset_name)
                index = array([ True if re.search(subset_pattern, attr_v) else False 
                                for attr_v in dataset[subset_attr] ])
            else:
                index = arange(dataset.size(), dtype='i')

            calib_datasets[dataset_name] = [dataset, calib_attr, index]

        init_v = array([], dtype='f8')
        for dataset_name, calib in calib_datasets.iteritems():
            dataset, calib_attr, index = calib
            if type(calib_attr) == str:
                init_v = np.concatenate((init_v, dataset[calib_attr][index]))
            elif type(calib_attr) in (list, tuple):
                for attr in calib_attr:
                    init_v = np.concatenate((init_v, dataset[attr][index]))
            else:
                raise TypeError, "Unrecongized data type in calib_datasets"

        t0 = time.time()

        if is_parallelizable==True: set_parallel(True)

        print OKBLUE+"\noptimizer = {} (is_parallel = {})".format(optimizer,is_parallelizable)+ENDC
        print OKBLUE+"-------------------------------------------------------\n"+ENDC
        if optimizer=='bfgs':
            default_kwargs = {'fprime': None, 
                      'epsilon': 1e-08,
                      'maxiter': None, 
                      'full_output': 1, 
                      'disp': 1, 
                      'retall': 0, 
                      'callback': None
                     }
            optimizer_func = fmin_bfgs
        elif optimizer=='lbfgsb':
            default_kwargs = {'fprime': None, 
                              'approx_grad': True,
                              'bounds': None,
                              'factr': 1e12,
                              'iprint': 1
                             }
            
            optimizer_func = fmin_l_bfgs_b
        elif optimizer=='anneal':
            default_kwargs = {'schedule': 'fast', 
                              'full_output': 1, 
                              'T0': None, 
                              'Tf': 1e-12, 
                              'maxeval': None, 
                              'maxaccept': None, 
                              'maxiter': 400, 
                              'boltzmann': 1.0, 
                              'learn_rate': 0.5, 
                              'feps': 1e-06, 
                              'quench': 1.0, 
                              'm': 1.0, 'n': 1.0, 
                              'lower': -1, 'upper': 1, 
                              'dwell': 50, 'disp': True
                             }

            optimizer_func = anneal
        elif optimizer=='panneal':
            default_kwargs = {'schedule': 'fast', 
                              'full_output': 1, 
                              'T0': None, 
                              'Tf': 1e-12, 
                              'maxeval': None, 
                              'maxaccept': None, 
                              'maxiter': 400, 
                              'boltzmann': 1.0, 
                              'learn_rate': 0.5, 
                              'feps': 1e-06, 
                              'quench': 1.0, 
                              'm': 1.0, 'n': 1.0, 
                              'lower': -1, 'upper': 1, 
                              'dwell': 50, 'disp': True,
                              'cores': 24, 'interv': 20
                             }

            optimizer_func = panneal
        else:
            raise ValueError, "Unrecognized optimizer {}".format(optimizer)

        default_kwargs.update(optimizer_kwargs)
        results = optimizer_func(self.target_func, copy(init_v), **default_kwargs)

        duration = time.time() - t0
        if results_pickle_prefix is not None:
            pickle_file = "{}_{}.pickle".format(results_pickle_prefix, optimizer)
            pickle_file = os.path.join(self.log_directory, pickle_file)
            pickle.dump(results, open(pickle_file, "wb"))

        if is_parallelizable == True: set_parallel(False)

        logger.log_status('init target_func: {}'.format(self.target_func(init_v)))
        logger.log_status('end target_func: {}'.format(results[:])) #which one?
        logger.log_status('outputs from optimizer: {}'.format(results))
        logger.log_status('Execution time: {}'.format(duration))

    def init_run(self, create_baseyear_cache=True):
        ''' init run, get run_id & cache_directory. '''
        ##avoid invoking start_run from cmd line - 
        option_group = StartRunOptionGroup()
        option_group.parser.set_defaults(xml_configuration=self.xml_config,
                                         scenario_name=self.scenario)
        #run_id, cache_directory = start_run(option_group)

        options, args = option_group.parse()
        self.run_manager = RunManager(option_group.get_services_database_configuration(options))

        resources = XMLConfiguration(self.xml_config).get_run_configuration(self.scenario)
        insert_auto_generated_cache_directory_if_needed(resources)
        cache_directory = resources['cache_directory']
        self.run_manager.setup_new_run(cache_directory, resources)
        run_id, cache_directory = self.run_manager.run_id, self.run_manager.get_current_cache_directory() 
        self.run_manager.add_row_to_history(run_id, resources, "done")

        if create_baseyear_cache:
            self.run_manager.create_baseyear_cache(resources)

        ## good for testing
        #run_id = 275
        #cache_directory = '/home/lmwang/opus/data/paris_zone/runs/run_275.2012_05_26_00_20'
        assert run_id is not None
        assert cache_directory is not None
        return run_id, cache_directory

    def update_parameters(self, est_v, cache_directory, simulation_state, dataset_pool, calib_datasets, *args, **kwargs):
        i_est_v = 0
        current_year = simulation_state.get_current_time()
        simulation_state.set_current_time(self.base_year)
        simulation_state.set_cache_directory(cache_directory)

        for dataset_name, calib in calib_datasets.iteritems():
            dataset, calib_attr, index = calib
            if type(calib_attr) == str:
                dtype = dataset[calib_attr].dtype
                dataset[calib_attr][index] = (est_v[i_est_v:i_est_v+index.size]).astype(dtype)
                i_est_v += index.size
            elif type(calib_attr) in (list, tuple):
                for attr in calib_attr:
                    dtype = dataset[attr].dtype
                    dataset[attr][index] = (est_v[i_est_v:i_est_v+index.size]).astype(dtype)
                    i_est_v += index.size
            else:
                raise TypeError, "Unrecongized data type in calib_datasets"
           
            #dtype = dataset[calib_attr].dtype
            #dataset[calib_attr][index] = (est_v[i_est_v:i_est_v+index.size]).astype(dtype)
            #flush dataset
            dataset.flush_dataset()
            #i_est_v += index.size
        simulation_state.set_current_time(current_year)

    def update_prediction(self, est_v, simulation_state, dataset_pool, calib_datasets, *args, **kwargs):
        option_group = RestartRunOptionGroup()
        option_group.parser.set_defaults(project_name=self.project_name,
                                         skip_cache_cleanup=self.skip_cache_cleanup)

        options, args = option_group.parse()
        if self.run_manager is None: 
           self.run_manager = RunManager(option_group.get_services_database_configuration(options))

        if lock!=None: lock.acquire()
        ## query runs available for re-use
        runs_done = self.run_manager.get_run_info(run_ids=self.run_ids, status='done') 
        create_baseyear_cache = False
        import pdb
        pdb.set_trace()
        if len(runs_done) == 0:  ##there is no re-usable run directory, init a new run
            run_id, cache_directory = self.init_run(create_baseyear_cache=False)
            self.run_ids.append(run_id)
            create_baseyear_cache = True
            logger.log_status('Initializing new run with id ' + str(run_id))
        else:
            run_id = runs_done[0].run_id ##take the first 'done' run_id
            cache_directory = self.run_manager.get_cache_directory(run_id)
            logger.log_status('Using old run with id ' + str(run_id))
        resources = self.run_manager.get_resources_for_run_id_from_history(run_id, 
                                                                  filter_by_status=False)
        self.run_manager.add_row_to_history(run_id, resources, "taken")
        if lock!=None: lock.release()

        if create_baseyear_cache:
            self.run_manager.create_baseyear_cache(resources)

        self.update_parameters(est_v, cache_directory, simulation_state, dataset_pool, calib_datasets, *args, **kwargs)
        restart_run(option_group=option_group, 
                    args=[run_id, self.start_year])

        prediction = self.summarize_prediction(cache_directory, simulation_state, dataset_pool, calib_datasets)
        return prediction

    def summarize_prediction(self, cache_directory, simulation_state, dataset_pool, calib_datasets):
        dataset_name = VariableName(self.target_expression).get_dataset_name()
        current_year = simulation_state.get_current_time()
        simulation_state.set_current_time(self.end_year)
        simulation_state.set_cache_directory(cache_directory)
        #force reload
        dataset_pool.remove_all_datasets()
        dataset = dataset_pool[dataset_name]
        ids = dataset.get_id_attribute()
        results = dataset.compute_variables(self.target_expression, 
                                            dataset_pool=dataset_pool)
        simulation_state.set_current_time(current_year)
        return dict(zip(ids, results))

    def read_target(self, target_file):
        ## read (& process) target numbers into a dictionary: {id:value}
        ## csv file with header 
        ## id, target
        header = file(target_file, 'r').readline().strip().split(',')
        contents = np.genfromtxt(target_file, delimiter=",", comments='#', skip_header=1)
        target = dict(zip(contents[:,0], contents[:,1]))

        return target

    def target_func(self, est_v, func=lambda x,y: np.sum(np.abs(x-y)), **kwargs):
        ''' Target function.'''

        simulation_state = SimulationState()
        simulation_state.set_current_time(self.base_year)
        simulation_state.set_cache_directory(self.cache_directory)
        attribute_cache = AttributeCache()
        dataset_pool = SessionConfiguration(new_instance=True,
                                  package_order=self.package_order,
                                  in_storage=attribute_cache
                                  ).get_dataset_pool()

        calib_datasets = {}
        for dataset_name, calib_attr in calib_datasets.iteritems():
            dataset = dataset_pool.get_dataset(dataset_name, 
                                                    dataset_arguments={'id_name':[]})
            assert subset is None or subset.get(dataset_name, None) is None or \
                   subset_patterns is None or subset_patterns.get(dataset_name, None) is None
            if subset is not None and subset.get(dataset_name, None) is not None:
                subset_attr, subset_cond = subset.get(dataset_name) 
                index = np.in1d(dataset[subset_attr], subset_cond)
            elif subset_patterns is not None and subset_patterns.get(dataset_name, None) is not None:
                subset_attr, subset_pattern = subset_patterns.get(dataset_name)
                index = array([ True if re.search(subset_pattern, attr_v) else False 
                                for attr_v in dataset[subset_attr] ])
            else:
                index = arange(dataset.size(), dtype='i')

            calib_datasets[dataset_name] = [dataset, calib_attr, index]

        prediction = self.update_prediction(est_v, simulation_state, dataset_pool, calib_datasets, **kwargs)
        ## allow keys in target not appearing in prediction
        ## assuming their values to be 0
        ### every key in target should appear in prediction
        #assert np.all( np.in1d(self.target.keys(), prediction.keys()) )
        target = np.array(self.target.values())
        predct = np.array([prediction[k] if prediction.has_key(k) else 0 \
                           for k in self.target.keys() ])
        results = func(predct, target)

        return results
    
if __name__ == "__main__":
    """
    from optparse import OptionParser
    desc="Tool script calibrates parameters in UrbanSim cache to meet specified targets"
    parser = OptionParser(description=desc)
    parser.add_option("-x", "--xml-config", dest="xml_config", default=None, 
                       help="file name of xml configuration (must also provide a scenario name using -s)")
    parser.add_option("-s", "--scenario", dest="scenario", default=None, 
                       help="name of the scenario to run")
    #parser.add_option("-d", "--calib-datasets", dest="calib_datasets", default=None, 
    #                   help="dictionary specifying datasets and attributes to be calibrated")
    parser.add_option("-d", "--calib-dataset", dest="calib_dataset", default=None, 
                       help="dataset to be calibrated")
    parser.add_option("-a", "--calib-attr", dest="calib_attr", default=None, 
                       help="attribute to be calibrated")
    parser.add_option("-t", "--target-expression", dest="target_expression", default=None, 
                       help="opus expression computing values from prediction to be compared with targets")
    parser.add_option("-f", "--target-file", dest="target_file", default=None, 
                       help="csv file providing targets")
    parser.add_option("--subset-attr", dest="subset_attr", default=None, 
                       help="dictionary specifying a subset of the calib_datasets to be calibrated")                   
    parser.add_option("--subset-vals", dest="subset_vals", default=None, 
                       help="values identifying a subset of the calib_datasets to be calibrated")                   
    parser.add_option("--subset-patterns", dest="subset_patterns", default=None, 
                       help="regular expression patterns identifying subset of the calib_datasets to be calibrated")                   
    #parser.add_option("--subset", dest="subset", default=None, 
    #                   help="dictionary specifying a subset of the calib_datasets to be calibrated")                   
    #parser.add_option("--subset-patterns", dest="subset_patterns", default=None, 
    #                   help="dictionary specifying regular expression patterns identifying subset of the calib_datasets to be calibrated")                   

    options, args = parser.parse_args()
    #required = ['xml_config', 'scenario', 'calib_datasets', 'target_expression', 'target_file']
    required = ['xml_config', 'scenario', 'calib_dataset', 'calib_attr', 'target_expression', 'target_file']
    for opt in required:
        if not options.__dict__[opt]:
            print "Mandatory option {} is missing\n".format(opt)
            parser.print_help()
            exit(-1)

    calib_datasets = {options.calib_dataset:options.calib_attr}
    subset, subset_pattersn = None, None
    if options.subset_vals is not None:
        subset = {options.calib_dataset: [options.subset_attr, options.subset_vals]}
    elif options.subset_patterns is not None:
        subset_patterns = {options.calib_dataset: [options.subset_attr, options.subset_patterns]}

    calib = Calibration(xml_config=options.xml_config, 
                        scenario=options.scenario, 
                        calib_datasets=calib_datasets, 
                        target_expression=options.target_expression,
                        target_file=options.target_file,
                        subset=subset,
                        subset_patterns=subset_patterns
                       )
    calib.run(results_pickle_prefix='calib')

    ## call with 
    python /home/lmwang/opus/src/opus_core/tools/start_calibration.py -x /home/atschirhar/opus/project_configs/paris_zone.xml -s paris_zone_calibration2 -d establishment_location_choice_model_coefficients -a estimate --subset-attr=coefficient_name --subset-patterns=*_celcm -t "zgpgroup.aggregate((establishment.employment)*(establishment.disappeared==0),intermediates=[building,zone,zgp])" -f /workspace/opus/data/paris_zone/temp_data/zgpgroup_totemp06.csv
    """
    

 
    try:
        calib_config = eval('calibration_{}'.format(sys.argv[1]))
    except NameError:
        sys.exit("Wrong argument '{}'. This calibration's configuration doesn't exist.".format(sys.argv[1]))

   
    calib = Calibration(xml_config        = calib_config['xml_config'],
                        scenario          = calib_config['scenario'],
                        calib_datasets    = calib_config['calib_datasets'],
                        target_expression = calib_config['target_expression'],
                        target_file       = calib_config['target_file'],
                        subset            = calib_config['subset'],
                        subset_patterns   = calib_config['subset_patterns'],
                        skip_cache_cleanup= calib_config['skip_cache_cleanup'],
                       )
   
    calib.run(optimizer=calib_config['optimizer'], results_pickle_prefix='calib', 
              optimizer_kwargs=calib_config.get('optimizer_kwargs', {}))
    
