# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

#from time import localtime, strftime
import datetime
from sqlalchemy.sql import select
from opus_core.misc import get_host_name
from opus_core.services.run_server.abstract_service import AbstractService

class ResultsManager(AbstractService):
    """An abstraction representing a simulation manager that automatically logs
    runs (and their status) to a database (run_activity),
    creates resources for runs, and can run simulations.
    """

    def __init__(self, options):
        AbstractService.__init__(self, options)
    
    def add_computed_indicator(self, indicator_name, dataset_name, expression, run_id, data_path, project_name):
        """update the run history table to indicate changes to the state of this run history trail."""
                
        values = {
             'run_id':run_id, 
             'indicator_name':str(indicator_name),
             'dataset_name':dataset_name,
             'expression':expression, 
             'data_path':data_path,
             'processor_name':get_host_name(),
             'date_time':datetime.datetime.now(),
             'project_name': project_name
             }        

        computed_indicators_table = self.services_db.get_table('computed_indicators')
        if not 'project_name' in computed_indicators_table.c:
            del values['project_name']
        qry = computed_indicators_table.insert(values = values)
        self.services_db.execute(qry)

    def get_results(self):
        host = get_host_name()
        tbl = self.services_db.get_table('computed_indicators')

        s = select([tbl.c.run_id,
                    tbl.c.indicator_name,
                    tbl.c.dataset_name,
                    tbl.c.expression,
                    tbl.c.data_path,
                    tbl.c.date_time],
                    whereclause = tbl.c.processor_name == host)
        results = []
        for run_id, indicator_name, dataset_name, expression, data_path, date_time \
            in self.services_db.execute(s).fetchall():
            res = {
                 'run_id':run_id, 
                 'indicator_name':indicator_name,
                 'dataset_name':dataset_name,
                 'expression':expression, 
                 'data_path':data_path,
                 'date_time':date_time,
                 }    
            results.append(res) 
        return results
    
from opus_core.tests import opus_unittest
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class ResultsManagerTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.database_name = 'test_services_database'
        self.config = TestDatabaseConfiguration(database_name = self.database_name)
        self.db_server = DatabaseServer(self.config)
    
    def tearDown(self):
        self.db_server.drop_database(self.database_name)
        self.db_server.close()
                
    def test_add_computed_indicator(self):
        result_manager = ResultsManager(self.config)
        
        indicator_name = 'test'
        dataset_name = 'ds'
        expression = 'exp'
        run_id = None
        data_path = '/home'        
        
        result_manager.add_computed_indicator(indicator_name, dataset_name, expression, run_id, data_path, project_name = 'test')
        
        db = self.db_server.get_database(self.database_name)
        computed_indicators_table = db.get_table('computed_indicators')
        
        s = select([computed_indicators_table.c.indicator_name,
                    computed_indicators_table.c.expression],
                    whereclause = computed_indicators_table.c.dataset_name == 'ds')

        results = db.execute(s).fetchall()
        self.assertEqual(len(results), 1)
        
        i_name, exp = results[0]
        self.assertEqual(indicator_name, i_name)
        self.assertEqual(expression, exp)
        
        result_manager.services_db.close()                
            
if __name__ == "__main__":
    opus_unittest.main()