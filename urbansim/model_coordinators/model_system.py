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

import os
import time

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
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.file_utilities import get_resources_from_file
from opus_core.store.scenario_database import ScenarioDatabase
from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.session_configuration import SessionConfiguration
from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration

# TODO: This file has syntax errors, is it working?
class ModelSystem(object):
    """
    Uses the information in configuration to run/estimate a set of models.
    """

    def run(self, resources, write_datasets_to_cache_at_end_of_year=True):
        """Entries in resources: (entries with no defaults are required)
               models - a list containing names of models to be run. Each name
                           must correspond to the name of the module/class of that model. Default(object): None
               years - a tuple (start year, end year)
               db_host_name - hostname of the mysql server. Default: "localhost"
               db_user_name - user name for the mysql server
               db_password - password for the mysql server
               db_input_database - name of the input database.
               db_output_database - name of the output database.
               debuglevel - an integer. The higher the more output will be printed. Default: 0
        """
        if not isinstance(resources, Resources):
            raise TypeError, "Argument 'resources' must be of type 'Resources'."
        logger_settings = resources.get("log", {"tags":[],
                                            "verbosity_level": 3})
        logger.set_tags(logger_settings.get("tags", []) )
        logger.set_verbosity_level(logger_settings.get("verbosity_level", 3))
        self.simulation_state = SimulationState()
        self.simulation_state.set_low_memory_run(resources.get("low_memory_mode", False))

        if resources['cache_directory'] is not None:
            self.simulation_state.set_cache_directory(resources['cache_directory'])

        cache_directory = self.simulation_state.get_cache_directory()
        log_file = os.path.join(cache_directory, 'run_multiprocess.log')
        logger.enable_file_logging(log_file, verbose=False)
        try:
            logger.log_status("Cache Directory set to: " + cache_directory)
            logger.start_block('Start simulation run')
            
            try:
                models = resources.get("models", None)
                models_in_years = resources.get("models_in_year",  {})
    
                if (not models) or (len(models) <=0):
                    logger.log_status("No models specified. Nothing to be run.")
                    return
    
                resources.check_obligatory_keys(["years"])
    
                years = resources["years"]
                if (not isinstance(years, tuple)) and (not isinstance(years, list)):
                    raise TypeError, "Entry 'years' in resources must be a tuple."
    
                if len(years) < 2:
                    print years
                    raise StandardError, "Entry 'years' in resources must be of length at least 2."
    
                start_year = years[0]
                end_year = years[-1]
                if not resources.has_key("flush_variables"): # if dependent attributes/variables should be flushed after each computation
                    resources["flush_variables"] = False
    
    
                if resources.has_key("flt_directory"):
                    flt_directory = resources["flt_directory"]
                else:
                    flt_directory = None
    
                # merge values in resources with defaults
                ### TODO: There is no good reason to be changing Configurations!
                self._merge_resources_with_defaults(resources)
    
                debuglevel = resources["debuglevel"]
    
                seed_values = resources['seed']
                logger.log_status("random seed = %s" % str(seed_values))
                seed(seed_values) # was: seed(seed_values[0], seed_values[1])
    
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
                                flt_directory=flt_directory,
                                write_datasets_to_cache_at_end_of_year=write_datasets_to_cache_at_end_of_year)
                        finally:
                            logger.enable_file_logging(log_file, verbose=False)
                        flt_directory = os.path.join(self.simulation_state.get_cache_directory(), str(year))
                        collect()
                    finally:
                        logger.end_block()
            finally:
                logger.end_block()

        finally:
            logger.disable_file_logging(log_file)

    def flush_datasets(self, dataset_names):
        dataset_pool = SessionConfiguration().get_dataset_pool()
        for dataset_name in dataset_names:
            if dataset_pool.has_dataset(dataset_name):
                self.flush_dataset(dataset_pool.get_dataset(dataset_name))

    def flush_dataset(self, dataset):
        """Write the PRIMARY attributes of this dataset to the cache."""
        if dataset and isinstance(dataset, Dataset):
            dataset.delete_computed_attributes()
            dataset.load_and_flush_dataset()

    def _merge_resources_with_defaults(self, resources):
        resources = resources.merge_with_defaults({
            "db_host_name":"localhost",
            "debuglevel":0,
            "constant_tables": ["urbansim_constants"],
            "seed":0,
            })

    def _get_database_connections(self, resources):
        if 'input_configuration' in resources:
            input_db = ScenarioDatabase(hostname = resources["input_configuration"].host_name,
                                        username = resources["input_configuration"].user_name,
                                        password = resources["input_configuration"].password,
                                        database_name = resources["input_configuration"].database_name)
        else:
            input_db = None
        if 'output_configuration' in resources:
            db_server = MysqlDatabaseServer(resources["output_configuration"])
            output_db = db_server.get_database(resources["output_configuration"].database_name)
            logger.log_status(
                'Outputing to database: %s on host %s' % (
                    resources["output_configuration"].database_name,
                    resources['output_configuration'].host_name,
                    ),
                tags=["database"],
                verbosity_level=1
                )
            if 'input_configuration' in resources:
                if db_server.has_database(resources["input_configuration"].database_name):
                    self._pre_populate_db_from_scenario(
                        input_db,
                        output_db,
                        input_config=resources["input_configuration"],
                        output_config=resources["output_configuration"],
                    )
        else:
            output_db = None
        return input_db, output_db

    def _pre_populate_db_from_scenario(self, input_db, output_db, input_config, output_config):
        """Copies to the output database the scenario tables needed for sql indicators.
        Also creates link to scenario database."""

        # Create a table pointing to scenario database for this output database.
        sql = ("drop table if exists input_scenario_information;"
               "create table `input_scenario_information` (scenario_database_url varchar(255), "
               "       urbansim_build_number varchar(255), run_date varchar(255) ); "
               "insert into input_scenario_information values ('jdbc:mysql://%s/%s', '(build ????)', '%s');") % (
                   input_config.host_name,
                   input_config.database_name,
                   time.asctime(),
               )
        output_db.DoQueries(sql)
        tables_to_copy = ['geographies',
                          'geography_names',
                          'gridcells_in_geography',
                         ]
        for table_name in tables_to_copy:
            if input_db.has_table(table_name):
                output_db.drop_table(table_name)
                sql = """create table %(output_db_name)s.%(table_name)s select * from $$.%(table_name)s""" % {
                    'table_name':table_name,
                    'output_db_name':output_config.database_name,
                }
                input_db.DoQuery(sql)
            else:
                logger.log_warning("Cannot copy table '%s' from input database '%s' to output database '%s'" % (
                    table_name,
                    input_config.database_name,
                    output_config.database_name,
                ))

    def _run_year(self, year, models, simulation_state, debuglevel,
                  resources, flt_directory, write_datasets_to_cache_at_end_of_year):
        """
        Assumes the large datasets resides in an flt cache.
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
                SessionConfiguration()["flush_variables"] = resources["flush_variables"]
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
                datasets = {} # TODO: eliminate need for this.
                for dataset_name, its_dataset in dataset_pool.datasets_in_pool().iteritems():
                    self.vardict[dataset_name] = its_dataset
                    datasets[dataset_name] = its_dataset
                    exec '%s=its_dataset' % dataset_name
    
                # This is needed. It resides in locals()
                # and is passed on to models as they run.
                ### TODO: There has got to be a better way!
                model_resources = Resources(datasets)
    
                #==========
                # Run the models.
                #==========
    
                for model_entry in models:
                    # list models can be in the form:
                    # [{'model_name_1': {'group_members': ['residential', 'commercial']}},
                    #  {'model_name_2': {'group_members': [{'residential': ['estimate','run']},
                    #                                      'commercial']}},
                    #  {'model_name_3': ['estimate', 'run']},
                    #  'model_name_4',
                    #  {'model_name_5': {'group_members': 'all'}}
                    # ]
                    model_group_members_to_run = {}
                    # get list of methods to be processed evtl. for each group member
                    if isinstance(model_entry, dict):
                        model_name = model_entry.keys()[0]
                        value = model_entry[model_name]
                        if isinstance(value, dict): # is a model group
                            if not value.keys()[0]=="group_members":
                                raise KeyError, "Key for model " + model_name + " must be 'group_members'."
                            group_members = value[value.keys()[0]]
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
                            for member in group_members:
                                if isinstance(member, dict): # see 'model_name_2' ('residential')
                                                             # in the comment above
                                    member_name = member.keys()[0]
                                    model_group_members_to_run[member_name] = member[member_name]
                                    if not isinstance(model_group_members_to_run[member_name], list):
                                        model_group_members_to_run[member_name]=[model_group_members_to_run[member_name]]
                                else: # see 'model_name_1'
                                    model_group_members_to_run[member] = ["run"]
                        else: # in the form 'model_name_3' in the comment above
                            processes = value
                            if not isinstance(processes, list):
                                processes = [processes]
                    else: # in the form 'model_name_4' in the comment above
                        model_name = model_entry
                        processes = ["run"]
    
                    group_member = None
                    for imember in range(max(1, len(model_group_members_to_run.keys()))):
                        controller_config = models_configuration[model_name]["controller"]
                        model_configuration = models_configuration[model_name]
                        if model_group_members_to_run.keys():
                            group_member_name = model_group_members_to_run.keys()[imember]
                            group_member = ModelGroupMember(model_group, group_member_name)
                            processes = model_group_members_to_run[group_member_name]
                            member_model_name = "%s_%s" % (group_member_name, model_name)
                            if member_model_name in models_configuration.keys():
                                model_configuration = models_configuration[member_model_name]
                                if "controller" in model_configuration.keys():
                                    controller_config = model_configuration["controller"]
    
                        # import part
                        if "import" in controller_config.keys():
                            import_config = controller_config["import"]
                            for import_module in import_config.keys():
                                exec("from %s import %s" % (import_module, import_config[import_module]))
    
                        # init part
                        model = self.do_init(locals())
    
                        # estimate and/or run part
                        for process in processes:
                            # prepare part
                            exec(self.do_prepare(locals()))
                            processmodel_config = controller_config[process]
                            if "output" in processmodel_config.keys():
                                outputvar = processmodel_config["output"]
                            else:
                                outputvar = "process_output"
                            self.vardict[outputvar] = self.do_process(locals())
                            exec outputvar+'=self.vardict[outputvar]'
    
                            # capture namespace for interactive estimation
                            self.run_year_namespace = locals()
                            self.flush_datasets(resources.get("datasets_to_cache_after_each_model",[]))
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
            model = eval("%s(%s)" %
                         (init_config["name"],
                          self.construct_arguments_from_config(init_config)))
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

    def run_multiprocess(self, resources):
        resources = Resources(resources)
        self._merge_resources_with_defaults(resources)

        if resources['cache_directory'] is not None:
            cache_directory = resources['cache_directory']
        else:
            cache_directory = SimulationState().get_cache_directory()

        ### TODO: Get rid of this! There is absolutely no good reason to be
        ###       changing the Configuration!
        resources['cache_directory'] = cache_directory

        if not os.path.exists(cache_directory):
            os.makedirs(cache_directory)

        log_file = os.path.join(cache_directory, 'run_multiprocess.log')
        logger.enable_file_logging(log_file)

        start_year = resources["years"][0]
        end_year = resources["years"][-1]
        nyears = end_year - start_year + 1
        root_seed = resources.get("seed", 0)
        seed(root_seed) #was: seed(root_seed[0], root_seed[1])
        seed_array = randint(1,2**30, 2*nyears)
        skip_first_year_of_urbansim = resources.get('skip_urbansim', False)

        logger.log_status("Running simulation for years %d thru %d" % (start_year, end_year))
        iyear = 0
        for year in range(start_year, end_year+1):
            if (year <> start_year) or ((year == start_year) and (not skip_first_year_of_urbansim)):
                logger.start_block('Running UrbanSim for year %d in new process' % year)
                try:
                    resources['years'] = (year, year)
                    resources['seed'] = seed_array[iyear], # was: (seed_array[iyear], seed_array[iyear+nyears])
                    logger.disable_file_logging(log_file)
                    ForkProcess().fork_new_process(
                        'urbansim.model_coordinators.model_system', resources)
                    logger.enable_file_logging(log_file, verbose=False)
                    resources["flt_directory"] = os.path.join(cache_directory, str(year))
                finally:
                    logger.end_block()

            if ('travel_model_configuration' in resources) and (not resources.get('skip_travel_model', False)):
                self._run_models_in_separate_processes(resources['travel_model_configuration'], year, resources)

            if 'post_year_configuration' in resources:
                self._run_models_in_separate_processes(resources['post_year_configuration'], year, resources)

            iyear +=1

        logger.log_status("Done running simulation for years %d thru %d" % (start_year, end_year))

    def _run_models_in_separate_processes(self, year_models_dict, year, resources):
        if year in year_models_dict:
            if 'models' in year_models_dict[year]:
                models = year_models_dict[year]['models']  #post_year_process format
            else:
                models = year_models_dict['models']  #travel model format
            for opus_path in models:
                ForkProcess().fork_new_process(opus_path,
                    resources, optional_args='-y %d' % year)

    def run_in_one_process(self, resources, run_in_background=False):
        resources = Resources(resources)
        self._merge_resources_with_defaults(resources)

        if resources['cache_directory'] is not None:
            cache_directory = resources['cache_directory']
        else:
            cache_directory = SimulationState().get_cache_directory()

        ### TODO: Get rid of this! There is no good reason to be changing the
        ###       Configuration.
        resources['cache_directory'] = cache_directory

        if not os.path.exists(cache_directory):
            os.makedirs(cache_directory)

        if run_in_background:
            optional_arguments = '&'
        else:
            optional_arguments = ''
        ForkProcess().fork_new_process(
                    'urbansim.model_coordinators.model_system', resources, delete_temp_dir=False,
                    optional_args=optional_arguments)

    def construct_arguments_from_config(self, config):
        key = "arguments"
        if (key not in config.keys()) or (len(config[key].keys()) <= 0):
            return ""
        arg_dict = config[key]
        result = ""
        for arg_key in arg_dict.keys():
            result += "%s=%s, " % (arg_key, arg_dict[arg_key])
        return result

if __name__ == "__main__":
    from opus_core.store.attribute_cache import AttributeCache

    from opus_core.session_configuration import SessionConfiguration

    try: import wingdbstub
    except: pass

    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-d", "--delete-resources-file-directory", dest="delete_resources_file_directory",
                      action="store_true",
                      help="Delete the directory containing the pickled resources file when done?")

    (options, args) = parser.parse_args()

    resources = Resources(get_resources_from_file(options.resources_file_name))

    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,
                         package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,
                         in_storage=AttributeCache())

    s = ModelSystem()
#    logger.enable_memory_logging()
    if not resources.get("log_to_stdout", True):
        logger.disable_std_out()
    if resources.has_key("only_convert_large_datasets_from_mysql_to_flt"):
        self._merge_resources_with_defaults(resources)
        s.cache_baseyear_data_from_mysql(resources)
    else:
        s.run(resources)

    if options.delete_resources_file_directory:
        dir = os.path.split(options.resources_file_name)[0]
        rmtree(dir)