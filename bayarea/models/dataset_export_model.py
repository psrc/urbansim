# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import re
from opus_core.logger import log_block
from opus_core.export_storage import ExportStorage
from opus_core.store.flt_storage import flt_storage
from opus_core.store.sql_storage import sql_storage
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

class DatasetExportModel(object):

    @log_block('Dataset Export Model')
    def run(self, table_names, 
            out_storage=None, 
            table_name_pattern=None,
            cache_directory=None, 
            year=None, 
            **kwargs):
        """
        export specified tables to database

        table_name_pattern: For example '{table_name}_{scenario_name}_{year}'
        """

        if not hasattr(self, 'out_storage'):
            if out_storage is None:
                raise ValueError, "Either out_storage argument needs to be specified or " + \
                        "prepare_for_run called before run method to create a valid out_storage."
            else:
                self.out_storage = out_storage
        sim_state = SimulationState()
        if sim_state.get_current_time() == 0:
            sim_state.set_current_time(9999) 
        if cache_directory is None:
            cache_directory = sim_state.get_cache_directory()
        
        attr_cache = AttributeCache(cache_directory=cache_directory)
        if year is None:
            years = attr_cache._get_sorted_list_of_years()
        else:
            assert isinstance(year, int)
            years = [year]

        for table_name in table_names:
            kwargs['table_name'] = table_name
            for year in years:
                kwargs['year'] = year
                out_table_name = table_name_pattern.format(**kwargs)
                in_storage = attr_cache.get_flt_storage_for_year(year)
                #cache_path = os.path.join(cache_directory, str(year))
                #in_storage = flt_storage(storage_location=cache_path)
                #TODO drop_table(table_name) if table_name exists
                ExportStorage().export_dataset(table_name, 
                                               in_storage=in_storage, 
                                               out_storage=self.out_storage,
                                               out_dataset_name=out_table_name)        
        self.post_run(kwargs['scenario_name'], years)

    def post_run(self, scenario_name, years):
        """call stored_procedure to post-process exported tables"""
        db = self.out_storage._get_db()
        scenario_name = re.sub('_', ' ', scenario_name)
        query_scen_id = "select id from scenario where name='{}'".format(scenario_name)
        scenario_id = db.execute(query_scen_id).fetchone()[0]
        min_year, max_year = min(years), max(years)
        query_st = "select create_urbansim_buildings({}, {}, {})".format(scenario_id,
                                                                        min_year,
                                                                        max_year)
        db.execute(query_st)

    def prepare_for_run(self, database_configuration, database_name):
        ## sql protocol, hostname, username and password are set in 
        ## $OPUS_HOME/settings/database_server_setting.xml
        db_config = DatabaseConfiguration(database_name=database_name,
                                          database_configuration=database_configuration)
        db_server = DatabaseServer(db_config)
        if not db_server.has_database(database_name): 
            db_server.create_database(database_name) 
        db = db_server.get_database(database_name)
        self.out_storage = sql_storage(storage_location=db)

        return self.out_storage

if __name__ == '__main__':
    from optparse import OptionParser
    import sys

    parser = OptionParser()
    parser.add_option('-c', '--cache_directory', 
                      dest='cache_directory',
                      type='string', 
                      help='The filesystem path to the cache to export (required).')
    parser.add_option('-C', "--database_configuration", dest="database_configuration", 
                      default = "estimation_database_server", action="store", 
                      help="Node name of the database server configuration in " + \
                      "database_server_configurations.xml where the output database is to be created (required).")
    parser.add_option('-d', '--database_name', dest='database_name', type='string', 
                      help='The name of the database to which output will be written (required).')
    parser.add_option('-t', '--table_name', dest='table_name', type='string', 
                      help='Name of table to be exported (required).')
    parser.add_option('-p', '--table_name_pattern', dest='table_name_pattern', type='string', 
                      default='{table_name}_{scenario_name}_{year}',
                      help='pattern of target table name, default={table_name}_{scenario_name}_{year}')
    parser.add_option('-r', '--run_id', dest='run_id', type='string', 
                      help='run_id value for use in table_name_pattern (optional)')
    parser.add_option('-s', '--scenario_name', dest='scenario_name', type='string', 
                      help='scenario_name value for use in table_name_pattern (optional)')
    
    options, args = parser.parse_args()
    if None in (options.cache_directory, options.database_configuration, 
                options.database_name):
        parser.print_help()
        sys.exit(0)

    dem = DatasetExportModel()
    dem.prepare_for_run(options.database_configuration,
                        options.database_name)
    dem.run([options.table_name],
            table_name_pattern=options.table_name_pattern,
            cache_directory=options.cache_directory,
            run_id=options.run_id,
            scenario_name=options.scenario_name)

