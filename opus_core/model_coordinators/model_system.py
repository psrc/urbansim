# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import time
import sys
import threading

from gc import collect

from shutil import rmtree
from optparse import OptionParser

from numpy import ones
from numpy import array
from numpy.random import seed
from numpy.random import randint

from opus_core.logger import logger
from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.model_group import ModelGroup
from opus_core.fork_process import ForkProcess
from opus_core.model_group import ModelGroupMember
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.file_utilities import get_resources_from_file
from opus_core.session_configuration import SessionConfiguration
from opus_core.variables.variable_factory import VariableFactory

NO_SEED = None

class ModelSystem(object):
    """
    Uses the information in configuration to run/estimate a set of models for given set of years.
    """

    def __init__(self):
        self.running = False
        self.forked_processes = []
        self.running_conditional = threading.Condition()

    def run(self, resources, write_datasets_to_cache_at_end_of_year=True, log_file_name='run_model_system.log',
            cleanup_datasets=True):
        """Entries in resources: (entries with no defaults are required)
               models - a list containing names of models to be run. Each name
                           must correspond to the name of the module/class of that model. Default(object): None
               years - a tuple (start year, end year)
               debuglevel - an integer. The higher the more output will be printed. Default: 0
               expression_library - a dictionary.  The keys in the dictionary are pairs (dataset_name, variable_name)
               and the values are the corresponding expressions.  The model system needs to set the expression library
               (if it isn't None) in DatasetFactory for DatasetFactory to know about variables defined as expressions
               in the xml expression library.  Default: None
        This method is called both to start up the simulation for all years, and also for each year
        when running with one process per year.  In the latter case, 'years' consists of just
        (current_year, current_year) rather than the real start and end years for the simulation.
        """
        if not isinstance(resources, Resources):
            raise TypeError, "Argument 'resources' must be of type 'Resources'."
        logger_settings = resources.get("log", {"tags":[],
                                            "verbosity_level": 3})
        logger.set_tags(logger_settings.get("tags", []) )
        logger.set_verbosity_level(logger_settings.get("verbosity_level", 3))
        self.simulation_state = SimulationState()
        self.simulation_state.set_low_memory_run(resources.get("low_memory_mode", False))
        self.simulation_state.set_start_time(resources.get("base_year", 0))
        self.run_year_namespace = {}

        if resources.get('cache_directory', None) is not None:
            self.simulation_state.set_cache_directory(resources['cache_directory'])

        if 'expression_library' in resources:
            VariableFactory().set_expression_library(resources['expression_library'])
            
        if resources.get('sample_input', False):
            self.update_config_for_multiple_runs(resources)

        cache_directory = self.simulation_state.get_cache_directory()
        log_file = os.path.join(cache_directory, log_file_name)
        logger.enable_file_logging(log_file, verbose=False)
        try:
            logger.log_status("Cache Directory set to: " + cache_directory)
            logger.start_block('Start simulation run')

            try:
                models = resources.get("models", [])
                models_in_years = resources.get("models_in_year",  {})

                resources.check_obligatory_keys(["years"])

                years = resources["years"]
                if (not isinstance(years, tuple)) and (not isinstance(years, list)):
                    raise TypeError, "Entry 'years' in resources must be a tuple."

                if len(years) < 2:
                    print years
                    raise StandardError, "Entry 'years' in resources must be of length at least 2."

                start_year = years[0]
                end_year = years[-1]

                debuglevel = resources.get("debuglevel", 0)
                seed_values = resources.get('seed', NO_SEED)

                logger.log_status("random seed = %s" % str(seed_values))
                seed(seed_values)

                for year in range(start_year, end_year+1):
                    logger.start_block("Starting simulation for year " + str(year))
                    try:
                        self.simulation_state.set_current_time(year)
                        SessionConfiguration().get_dataset_pool().remove_all_datasets()
                        logger.disable_file_logging(log_file)
                        try:
                            if models_in_years.get(year, None) is not None:
                                models_to_run = models_in_years[year]
                            else:
                                models_to_run = models
                            self._run_year(
                                year=year,
                                models=models_to_run,
                                simulation_state=self.simulation_state,
                                debuglevel=debuglevel,
                                resources=resources,
                                write_datasets_to_cache_at_end_of_year=write_datasets_to_cache_at_end_of_year,
                                cleanup_datasets=cleanup_datasets)
                        finally:
                            logger.enable_file_logging(log_file, verbose=False)
                        collect()
                    finally:
                        logger.end_block()
            finally:
                logger.end_block()

        finally:
            logger.disable_file_logging(log_file)

    def flush_datasets(self, dataset_names, after_model=False):
        dataset_pool = SessionConfiguration().get_dataset_pool()
        for dataset_name in dataset_names:
            if dataset_pool.has_dataset(dataset_name):
                self.flush_dataset(dataset_pool.get_dataset(dataset_name), after_model=after_model)

    def flush_dataset(self, dataset, after_model=False):
        """Write the PRIMARY attributes of this dataset to the cache."""
        if dataset and isinstance(dataset, Dataset):
            # Do not flush after model if not necessary
            if after_model:
                if len(dataset.get_attribute_names()) <= len(dataset.get_id_name()):
                    return
                if (len(dataset.get_attribute_names()) == len(dataset.get_known_attribute_names())) and \
                                         (len(dataset.get_attributes_in_memory()) <= len(dataset.get_id_name())):
                    dataset.delete_computed_attributes()
                    return
            dataset.delete_computed_attributes()
            dataset.load_and_flush_dataset()

    def flush_datasets_after_model(self, resources):
        if resources.get('flush_variables', False):
            AttributeCache().delete_computed_tables()
            # this will also delete computed attributes
            datasets_to_cache = SessionConfiguration().get_dataset_pool().datasets_in_pool().keys()
        else:
            datasets_to_cache = resources.get("datasets_to_cache_after_each_model",[])
        self.flush_datasets(datasets_to_cache, after_model=True)
        
    def _run_year(self, year, models, simulation_state, debuglevel,
                  resources, write_datasets_to_cache_at_end_of_year, cleanup_datasets=True):
        """
        Assumes that all datasets resides in the cache directory in binary format.
        """
        try: import wingdbstub
        except: pass
        self.vardict = {}
        log_file_name = os.path.join(simulation_state.get_cache_directory(),
                                     "year_%s_log.txt" % year)
        logger.enable_file_logging(log_file_name, 'w')
        try:
            logger.start_block('Simulate year %s' % year)
            try:
                base_year = resources['base_year']
                if year == base_year:
                    year_for_base_year_cache = year # case of estimation
                else:
                    year_for_base_year_cache = year - 1
                cache_storage = AttributeCache().get_flt_storage_for_year(year_for_base_year_cache)
                self.vardict['cache_storage'] = cache_storage
                base_cache_storage = AttributeCache().get_flt_storage_for_year(base_year)
                self.vardict['base_cache_storage'] = base_cache_storage
                simulation_state.set_flush_datasets(resources.get("flush_variables", False))
                SessionConfiguration()["simulation_year"] = year
                SessionConfiguration()["debuglevel"] = debuglevel
                datasets_to_preload_in_year = resources.get('datasets_to_preload_in_year',{})
                if datasets_to_preload_in_year.get(year, None) is not None:
                    datasets_to_preload = datasets_to_preload_in_year[year]
                else:
                    datasets_to_preload = resources.get('datasets_to_preload',{})
                for dataset_name in datasets_to_preload:
                    SessionConfiguration().get_dataset_from_pool(dataset_name)
                models_configuration = resources['models_configuration']
                dataset_pool = SessionConfiguration().get_dataset_pool()
                datasets = {}
                for dataset_name, its_dataset in dataset_pool.datasets_in_pool().iteritems():
                    self.vardict[dataset_name] = its_dataset
                    datasets[dataset_name] = its_dataset
                    exec '%s=its_dataset' % dataset_name

                # This is needed. It resides in locals()
                # and is passed on to models as they run.
                ### TODO: There has got to be a better way!
                model_resources = Resources(datasets)
                n_models, model_group_members_to_run = self.get_number_of_models_and_model_group_members_to_run(models, models_configuration)
                self.run_year_namespace = locals()
                #==========
                # Run the models.
                #==========
                model_number = -1
                for model_entry in models:
                    # list 'models' can be in the form:
                    # [{'model_name_1': {'group_members': ['residential', 'commercial']}},
                    #  {'model_name_2': {'group_members': [{'residential': ['estimate','run']},
                    #                                      'commercial']}},
                    #  {'model_name_3': ['estimate', 'run']},
                    #  'model_name_4',
                    #  {'model_name_5': {'group_members': 'all'}}
                    # ]
                    # get list of methods to be processed evtl. for each group member
                    if isinstance(model_entry, dict):
                        model_name, value = model_entry.items()[0]
                        if not isinstance(value, dict): # is a model group
                            processes = value
                            if not isinstance(processes, list):
                                processes = [processes]
                    else: # in the form 'model_name_4' in the comment above
                        model_name = model_entry
                        processes = ["run"]
                    group_member = None
                    model_group = model_group_members_to_run[model_name][1]
                    last_member = max(1, len(model_group_members_to_run[model_name][0].keys()))
                    for imember in range(last_member):
                        controller_config = models_configuration[model_name]["controller"]
                        model_configuration = models_configuration[model_name]
                        if model_group_members_to_run[model_name][0].keys():
                            group_member_name = model_group_members_to_run[model_name][0].keys()[imember]
                            group_member = ModelGroupMember(model_group, group_member_name)
                            processes = model_group_members_to_run[model_name][0][group_member_name]
                            member_model_name = "%s_%s" % (group_member_name, model_name)
                            if member_model_name in models_configuration.keys():
                                model_configuration = models_configuration[member_model_name]
                                if "controller" in model_configuration.keys():
                                    controller_config = model_configuration["controller"]
                        datasets_to_preload_for_this_model = controller_config.get('_model_structure_dependencies_',{}).get('dataset',[])
                        for dataset_name in datasets_to_preload_for_this_model:
                            try:
                                if not dataset_pool.has_dataset(dataset_name):
                                    ds = dataset_pool.get_dataset(dataset_name)
                                    self.vardict[dataset_name] = ds
                                    datasets[dataset_name] = ds
                                    exec '%s=ds' % dataset_name
                            except:
                                logger.log_warning('Failed to load dataset %s.' % dataset_name)
                        # import part
                        if "import" in controller_config.keys():
                            import_config = controller_config["import"]
                            for import_module in import_config.keys():
                                exec("from %s import %s" % (import_module, import_config[import_module]))

                        # gui_import_replacements part
                        # This is a temporary hack -- replicates the functionality of the "import" section
                        # for use with the GUI.  The contents of this part of the config is a dictionary.
                        # Keys are names of models (not used here).  Values are 2 element pairs.
                        # The first element is a name and the second is a value.  Bind the name to the value.
                        if "gui_import_replacements" in controller_config.keys():
                            import_replacement_config = controller_config["gui_import_replacements"]
                            for model_name in import_replacement_config.keys():
                                pair = import_replacement_config[model_name]
                                temp = pair[1]
                                exec("%s = temp") % pair[0]

                        # init part
                        model = self.do_init(locals())

                        # estimate and/or run part
                        for process in processes:
                            model_number = model_number+1
                            # write status file
                            model.set_model_system_status_parameters(year, n_models, model_number, resources.get('status_file_for_gui', None))
                            model.write_status_for_gui()
                            # prepare part
                            exec(self.do_prepare(locals()))
                            processmodel_config = controller_config[process]
                            if "output" in processmodel_config.keys():
                                outputvar = processmodel_config["output"]
                            else:
                                outputvar = "process_output"
                            self.vardict[outputvar] = self.do_process(locals())
                            exec outputvar+'=self.vardict[outputvar]'

                            # check command file from gui, if the simulation should be stopped or paused
                            self.do_commands_from_gui(resources.get('command_file_for_gui', None))

                            # capture namespace for interactive estimation
                            self.run_year_namespace = locals()
                            self.flush_datasets_after_model(resources)
                            del model
                            collect()

                # Write all datasets to cache.
                if write_datasets_to_cache_at_end_of_year:
                    logger.start_block('Writing datasets to cache for year %s' % year)
                    try:
                        for dataset_name, its_dataset in SessionConfiguration().get_dataset_pool().datasets_in_pool().iteritems():
                            self.flush_dataset(its_dataset)
                    finally:
                        logger.end_block()

            finally:
                logger.end_block()
        finally:
            logger.disable_file_logging(log_file_name)

        if cleanup_datasets:
            SessionConfiguration().delete_datasets()

    def do_init(self, parent_state):
        """Run the 'init' part of this model's configuration.
        Returns model object.
        """
        # give this method the same local variables as its calling method has.
        for key in parent_state.keys():
            if key <> 'self':
                exec('%s = parent_state["%s"]' % (key, key))
        init_config = parent_state['controller_config']["init"]
        group_member = parent_state['group_member']
        if group_member is None: # No model group
            cmd = "%s(%s)" % (init_config["name"],
                          self.construct_arguments_from_config(init_config))
            model = eval(cmd)
        else: # Model belongs to a group
            model = eval("%s(group_member, %s)" %
                         (init_config["name"],
                          self.construct_arguments_from_config(init_config)))
        return model

    def do_prepare(self, parent_state):
        """Prepares for the current model in the parent state's context.
        What to do is determined by the contents of the current model's controller configuration.

        controller_config is the 'controller' part of the model configuration.
        vardict is a dictionary into which the output of the model's 'prepare_output'
        method will be put.
        """
        # give this method the same local variables as its calling method has.
        for key in parent_state.keys():
            if key <> 'self':
                exec('%s = parent_state["%s"]' % (key, key))
        key_name = "prepare_for_%s" % process
        if key_name in controller_config.keys():
            prepare_config = controller_config[key_name]
            if "output" in prepare_config.keys():
                outputvar = prepare_config["output"]
            else:
                outputvar = "prepare_output"
            self.vardict[outputvar] = eval("model.%s(%s)" %
                                      (prepare_config["name"],
                                       self.construct_arguments_from_config(prepare_config)))
            return '%s=self.vardict["%s"]' % (outputvar, outputvar)
        else:
            # do nothing when return value is exec'ed
            return ''

    def do_process(self, parent_state):
        for key in parent_state.keys():
            if key <> 'self':
                exec('%s = parent_state["%s"]' % (key, key))
        ev = "model.%s(%s)" % (process,
                               self.construct_arguments_from_config(processmodel_config))
        return eval(ev)

    def get_number_of_models_and_model_group_members_to_run(self, models, models_configuration):
        """Count number_of models in the list 'models' that can include group members (each member and each process is one model)."""
        # list models can be in the form:
        # [{'model_name_1': {'group_members': ['residential', 'commercial']}},
        #  {'model_name_2': {'group_members': [{'residential': ['estimate','run']},
        #                                      'commercial']}},
        #  {'model_name_3': ['estimate', 'run']},
        #  'model_name_4',
        #  {'model_name_5': {'group_members': 'all'}}
        # ]
        number_of_models = 1
        model_group_members_to_run = {}
        for model_entry in models:
            if isinstance(model_entry, dict):
                model_name, value = model_entry.items()[0]
                if isinstance(value, dict): # is a model group
                    if not value.keys()[0]=="group_members":
                        raise KeyError, "Key for model " + model_name + " must be 'group_members'."
                    group_members = value["group_members"]
                    model_group = None
                    if 'group_by_attribute' in models_configuration[model_name]["controller"].keys():
                        group_dataset_name, group_attribute = models_configuration[model_name]["controller"]['group_by_attribute']
                        model_group = ModelGroup(SessionConfiguration().get_dataset_from_pool(group_dataset_name),
                                             group_attribute)
                    if not isinstance(group_members, list):
                        group_members = [group_members]
                    if group_members[0] == "_all_": # see 'model_name_5' example above
                        if model_group is None:
                            raise KeyError, "Entry 'group_by_attribute' is missing for model %s" % model_name
                        group_members = model_group.get_member_names()
                    model_group_members_to_run[model_name] = [{}, model_group]
                    for member in group_members:
                        if isinstance(member, dict):
                            # see 'model_name_2' ('residential') in the comment above
                            member_name = member.keys()[0]
                            model_group_members_to_run[model_name][0][member_name] = member[member_name]
                            if not isinstance(model_group_members_to_run[model_name][0][member_name], list):
                                model_group_members_to_run[model_name][0][member_name]=[model_group_members_to_run[model_name][0][member_name]]
                            number_of_models +=len(model_group_members_to_run[model_name][0][member_name])
                        else: # see 'model_name_1'
                            model_group_members_to_run[model_name][0][member] = ["run"]
                            number_of_models +=len(model_group_members_to_run[model_name][0][member])
                else: # in the form 'model_name_3' in the comment above
                    model_group_members_to_run[model_name] = [{}, None]
                    if not isinstance(value, list):
                        number_of_models +=1
                    else:
                        number_of_models += len(value)
            else: # in the form 'model_name_4' in the comment above
                model_group_members_to_run[model_entry] = [{}, None]
                number_of_models +=1
        return  (number_of_models, model_group_members_to_run)

    def do_commands_from_gui(self, filename=None):
        if (filename is None) or not os.path.exists(filename):
            return
        while True:
            f = file(filename)
            line = f.read().strip()
            f.close()
            if line == 'stop':
                logger.log_warning('Simulation stopped.')
                sys.exit()
            elif line == 'resume':
                break
            elif line <> 'pause':
                logger.log_warning("Unknown command '%s'. Allowed commands: 'stop', 'pause', 'resume'." % line)
            time.sleep(10)


    def run_multiprocess(self, resources):
        resources = Resources(resources)
        profiler_name = resources.get("profile_filename", None)
        if resources['cache_directory'] is not None:
            cache_directory = resources['cache_directory']
        else:
            cache_directory = SimulationState().get_cache_directory()

        ### TODO: Get rid of this! There is absolutely no good reason to be
        ###       changing the Configuration!
        resources['cache_directory'] = cache_directory

        log_file = os.path.join(cache_directory, 'run_multiprocess.log')
        logger.enable_file_logging(log_file)

        start_year = resources["years"][0]
        end_year = resources["years"][-1]
        nyears = end_year - start_year + 1
        root_seed = resources.get("seed", NO_SEED)
        if resources.get('_seed_dictionary_', None) is not None:
            # This is added by the RunManager to ensure reproducibility including restarted runs 
            seed_dict = resources.get('_seed_dictionary_')
            seed_array = array(map(lambda year : seed_dict[year], range(start_year, end_year+1)))
        else:
            seed(root_seed)
            seed_array = randint(1,2**30, nyears)
        logger.log_status("Running simulation for years %d thru %d" % (start_year, end_year))
        logger.log_status("Simulation root seed: %s" % root_seed)

        for iyear, year in enumerate(range(start_year, end_year+1)):
            success = self._run_each_year_as_separate_process(iyear, year, 
                                                                 seed=seed_array[iyear],
                                                                 resources=resources,
                                                                 profiler_name=profiler_name,
                                                                 log_file=log_file)
            if not success:
                break

        self._notify_stopped()
        if profiler_name is not None: # insert original value
            resources["profile_filename"] = profiler_name
        logger.log_status("Done running simulation for years %d thru %d" % (start_year, end_year))

    #TODO: changing of configuration
    def _run_each_year_as_separate_process(self, iyear, year, 
                                           seed=None, 
                                           resources=None, 
                                           profiler_name=None,
                                           log_file=None):

        logger.start_block('Running simulation for year %d in new process' % year)
        resources['years'] = (year, year)
        resources['seed'] = seed,

        if profiler_name is not None:
            # add year to the profile name
            resources["profile_filename"] = "%s_%s" % (profiler_name, year)
            
        optional_args = []
        if log_file:
            optional_args += ['--log-file-name', os.path.split(log_file)[-1]]
        
        success = False
        try:
            logger.disable_file_logging(log_file)
            success = self._fork_new_process(
                'opus_core.model_coordinators.model_system', 
                resources, optional_args=optional_args)
            logger.enable_file_logging(log_file, verbose=False)
        finally:
            logger.end_block()
            
        return success

    def run_in_one_process(self, resources, run_in_background=False, class_path='opus_core.model_coordinators.model_system'):
        resources = Resources(resources)
        if resources['cache_directory'] is not None:
            cache_directory = resources['cache_directory']
        else:
            cache_directory = SimulationState().get_cache_directory()

        ### TODO: Get rid of this! There is no good reason to be changing the
        ###       Configuration.
        resources['cache_directory'] = cache_directory

        self._fork_new_process(
            '%s' % class_path, resources, delete_temp_dir=False, run_in_background=run_in_background)
        self._notify_stopped()

    def run_in_same_process(self, resources, **kwargs):
        resources = Resources(resources)
        if resources['cache_directory'] is not None:
            cache_directory = resources['cache_directory']
        else:
            cache_directory = SimulationState().get_cache_directory()

        ### TODO: Get rid of this! There is no good reason to be changing the
        ###       Configuration.
        resources['cache_directory'] = cache_directory

        self._notify_started()
        RunModelSystem(model_system = self, resources = resources, **kwargs)
        self._notify_stopped()

    def construct_arguments_from_config(self, config):
        key = "arguments"
        if (key not in config.keys()) or (len(config[key].keys()) <= 0):
            return ""
        arg_dict = config[key]
        result = ""
        for arg_key in arg_dict.keys():
            result += "%s=%s, " % (arg_key, arg_dict[arg_key])
        return result

    def wait_for_start(self):
        self.running_conditional.acquire()
        while not self.running:
            self.running_conditional.wait()
        self.running_conditional.release()

    def wait_for_finish(self):
        self.running_conditional.acquire()
        while self.running:
            self.running_conditional.wait()
        self.running_conditional.release()

    def wait_for_process_or_finish(self, process_index):
        self.running_conditional.acquire()
        while process_index >= len(self.forked_processes) and self.running:
            self.running_conditional.wait()
        self.running_conditional.release()
        if not self.running:
            process_index = len(self.forked_processes)-1
        return process_index

    def _fork_new_process(self, module_name, resources, run_in_background=False, **key_args):
        self.running_conditional.acquire()
        self.running = True
        self.forked_processes.append(ForkProcess())
        key_args["run_in_background"] = run_in_background
        success = self.forked_processes[-1].fork_new_process(module_name, resources, **key_args)
        self.running_conditional.notifyAll()
        self.running_conditional.release()
        if not run_in_background:
            self.forked_processes[-1].wait()
            self.forked_processes[-1].cleanup()
        return success

    def _notify_started(self):
        self.running_conditional.acquire()
        self.running = True
        self.running_conditional.notifyAll()
        self.running_conditional.release()

    def _notify_stopped(self):
        self.running_conditional.acquire()
        self.running = False
        self.running_conditional.notifyAll()
        self.running_conditional.release()

    def update_config_for_multiple_runs(self, config):
        models_to_update = config.get('models_with_sampled_coefficients', [])
        if 'models_in_year' not in config.keys():
            config['models_in_year'] = {}
        if config['models_in_year'].get(config['base_year']+1, None) is None:
            config['models_in_year'][config['base_year']+1]= config.get('models')
        
        for umodel in models_to_update:
            try:
                i = config['models_in_year'][config['base_year']+1].index(umodel)
                new_model_name = '%s_sampled_coef' % umodel
                config['models_in_year'][config['base_year']+1][i] = new_model_name
            except:
                pass
            config["models_configuration"][new_model_name] = Configuration(config["models_configuration"][umodel])
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["sample_coefficients"] = True
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["distribution"] = "'normal'"
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["cache_storage"] = "base_cache_storage" 
    
class RunModelSystem(object):
    def __init__(self, model_system, resources, skip_cache_after_each_year = False, log_file_name = 'run_model_system.log'):

        SessionConfiguration(new_instance=True,
                             package_order=resources['dataset_pool_configuration'].package_order,
                             in_storage=AttributeCache())

    #    logger.enable_memory_logging()
        if not resources.get("log_to_stdout", True):
            logger.disable_std_out()

        profiler = None
        if resources.get("profile_filename", None) is not None:
            import hotshot
            profiler = hotshot.Profile(resources.get("profile_filename"))

        write_datasets_to_cache_at_end_of_year = not skip_cache_after_each_year

        if profiler is None:
            model_system.run(resources, write_datasets_to_cache_at_end_of_year=write_datasets_to_cache_at_end_of_year, log_file_name=log_file_name)
        else:
            profiler.run("model_system.run(resources, write_datasets_to_cache_at_end_of_year=write_datasets_to_cache_at_end_of_year, log_file_name=log_file_name)")
            logger.log_status('Profiling data stored in %s. Use the python module hotshot to view them.' %
                                  resources.get("profile_filename"))
            profiler.close()

def main(model_system_class):
    s = model_system_class()
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-d", "--delete-resources-file-directory", dest="delete_resources_file_directory",
                      action="store_true",
                      help="Delete the directory containing the pickled resources file when done?")
    parser.add_option("--skip-cache-after-each-year", dest="skip_cache_after_each_year", default=False,
                      action="store_true", help="Datasets will not be cached at the end of each year.")
    parser.add_option("--log-file-name", dest="log_file_name", default='run_model_system.log',
                      help="File name for logging output of model system (without directory).")

    (options, args) = parser.parse_args()

    resources = Resources(get_resources_from_file(options.resources_file_name))
    delete_resources_file_directory = options.delete_resources_file_directory
    skip_cache_after_each_year = options.skip_cache_after_each_year
    log_file_name = options.log_file_name
    RunModelSystem(model_system = s,
                   resources = resources,
                   skip_cache_after_each_year = skip_cache_after_each_year,
                   log_file_name = log_file_name)
    if delete_resources_file_directory:
        dir = os.path.split(options.resources_file_name)[0]
        rmtree(dir)

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    main(ModelSystem)