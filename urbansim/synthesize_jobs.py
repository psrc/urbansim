# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.misc import sample
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.flatten_scenario_database_chain import FlattenScenarioDatabaseChain
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

class SynthesizeJobs(object):
    def synthesize_employment_data(self, config):
        """
        Synthesize employment data and output a new database with the added job 
        data.
        
        Assumes all databases are on the same database server.
        """
        jobs_by_zone_by_sector_table_name = config['jobs_by_zone_by_sector']
        gridcells_table_name = config['gridcells']
        jobs_table_name = config['jobs']
        gridcells_output_table_name = config['gridcells_output']
        jobs_output_table_name = config['jobs_output']
        
        input_db_name = config['db_config'].database_name
        output_db_name = config['output_database_name']
        
        sectors = config['sector_names_and_ids']
        building_types_and_ids_and_home_based = config[
                            'building_type_column_names_and_ids_and_home_based']
            
        building_types = []
        building_ids = []
        home_based = []                            
        for type, id, home in building_types_and_ids_and_home_based:
            building_types += [type]
            building_ids += [id]
            home_based += [home]
                    
        
        from_database_configuration = ScenarioDatabaseConfiguration(
                                            database_name = input_db_name,
                                            host_name = config['db_config'].host_name,
                                            user_name = config['db_config'].user_name,
                                            password = config['db_config'].password                                            
                                        )
        to_database_configuration = ScenarioDatabaseConfiguration(
                                            database_name = output_db_name,
                                            host_name = config['db_config'].host_name,
                                            user_name = config['db_config'].user_name,
                                            password = config['db_config'].password                                            
                                        )

        FlattenScenarioDatabaseChain().copy_scenario_database(
                              from_database_configuration = from_database_configuration, 
                              to_database_configuration = to_database_configuration,
                              tables_to_copy = [gridcells_table_name, jobs_table_name])
        
        db_server = DatabaseServer(to_database_configuration)       
        output_database = db_server.get_database(output_db_name)
                
        sector_name = 0; sector_id = 1
        
        sector = {}
        for entry in sectors:
            name = entry[sector_name]
            id = entry[sector_id]
            sector[id] = self._get_jobs_per_building_type_in_sector_by_zone(
                output_database, jobs_by_zone_by_sector_table_name, 
                jobs_table_name, name, id)

        results = self._get_building_type_proportion_by_zone(output_database, 
                                                           gridcells_table_name)
            
        grid_id = 0; zone_id = 1
        dist = {}
        
        type_index = {}
        
        for name in building_types:
            for i in range(len(results[0])):
                column_name = results[0][i]
                if name == column_name:
                    type_index[name] = i
                    break;
            else:
                raise KeyError, ('No column by the name of \'%s\' found in '
                                 'the database.' % name)  

        for name in building_types:
            dist[name] = {}
        
        for row in results[1:]:
            for name in building_types:
                dist[name][row[zone_id]] = []
            
        for row in results[1:]:
            for name in building_types:
                dist[name][row[zone_id]] += [(row[grid_id], 
                                              row[type_index[name]])]
        
        jobs_table_data = self._create_jobs_table_data(dist, sector,
                                          building_types_and_ids_and_home_based)
        
        output_database.execute('USE %(out_db)s' % {'out_db':output_db_name})
        
        output_database.execute("""
            CREATE TABLE %(jobs_out)s (
                JOB_ID INT AUTO_INCREMENT, PRIMARY KEY(JOB_ID),
                GRID_ID INT, HOME_BASED INT, SECTOR_ID INT, BUILDING_TYPE INT);
            """ % {'jobs_out':jobs_output_table_name})
        
        if len(jobs_table_data) > 0:
            output_prefix = (
                """INSERT INTO %(jobs_out)s 
                    (GRID_ID, HOME_BASED, SECTOR_ID, BUILDING_TYPE) VALUES
                """ % {'jobs_out':jobs_output_table_name})
            output_postfix = ';'
            
            step = 1000
            length = len(jobs_table_data)
            iterations = int(length/step) + 1
            
            for i in range(iterations):
                low = i*step
                high = (i+1)*step
                
                if high > length: high = length
                
                output_body = ""
                
                for j in range(low, high):
                    output_body += (
                        '(%(grid)s, %(home)s, %(sector)s, %(building)s),\n' 
                        % jobs_table_data[j])
                
                output_query = "%s%s%s" % (output_prefix, 
                                           output_body[:-2], 
                                           output_postfix)

                output_database.execute(output_query)
                
            
            ### TODO: 
#        output_database.execute("""
#            CREATE TABLE %(grid_out)s SELECT * FROM %(in_db)s.%(grid)s
#            """ % {'grid_out':gridcells_output_table_name,
#                   'in_db':input_db_name,
#                   'grid':gridcells_table_name})
#       
#        output_database.execute("""
#        
#            SELECT g.GRID_ID, COUNT, BUILDING_TYPE, COMMERCIAL_SQFT, INDUSTRIAL_SQFT
#            FROM washtenaw_baseyear.gridcells AS g,
#                 (SELECT GRID_ID, COUNT(*) AS COUNT, BUILDING_TYPE
#                 FROM jobs
#                 WHERE BUILDING_TYPE = 1 OR BUILDING_TYPE = 3
#                 GROUP BY GRID_ID, BUILDING_TYPE) as j
#            WHERE g.GRID_ID = j.GRID_ID
#            
#            """ % {'grid_out':gridcells_output_table_name,
#                   'jobs_out':jobs_output_table_name})
            
        
    
    def _get_jobs_per_building_type_in_sector_by_zone(self, db, 
        jobs_by_zone_by_sector_table_name, jobs_table_name, type, sector):
        """
        [Internal]
        Queries the given database tables for the building types and number of
        jobs for that building type and returns a list of them as tuples.
        """
            
        jobs_per_building_type = {}
        total_jobs = {}
        
        results = db.GetResultsFromQuery(
            """SELECT taz AS ZONE,
                BUILDING_TYPE, 
                %(type)s*PROPORTION AS JOBS_FOR_THIS_TYPE,
                %(type)s AS TOTAL
            FROM %(data)s AS d,
                (SELECT j.SECTOR_ID, BUILDING_TYPE, RAW/TOTAL AS PROPORTION 
                FROM (SELECT SECTOR_ID, BUILDING_TYPE, COUNT(*) AS RAW 
                     FROM %(jobs)s 
                     GROUP BY SECTOR_ID, BUILDING_TYPE) AS j, 
                     
                     (SELECT SECTOR_ID,COUNT(*) AS TOTAL 
                     FROM %(jobs)s 
                     GROUP BY SECTOR_ID) AS t
                WHERE j.SECTOR_ID = t.SECTOR_ID) AS p
            WHERE p.SECTOR_ID = %(sector)s
            ORDER BY ZONE
            """ % {'type':type,
                   'sector':sector,
                   'data':jobs_by_zone_by_sector_table_name,
                   'jobs':jobs_table_name})  

        zone = 0; building_type = 1; jobs_for_this_type = 2; total = 3
        for row in results[1:]:
            jobs_per_building_type[row[zone]] = []
        
        for row in results[1:]:
            jobs_per_building_type[row[zone]] += [(row[building_type], 
                                                   row[jobs_for_this_type])]
            total_jobs[row[zone]] = row[total];
                                                   
        for key in jobs_per_building_type.keys():
            jobs_per_building_type[key] = self._resolve_fractional_jobs(
                                   jobs_per_building_type[key], total_jobs[key])       
        return jobs_per_building_type
    
    
    def _resolve_fractional_jobs(self, zone_building_type_and_jobs_list, total):
        """
        [Internal]
        Takes a list of tuples of building types and fractional jobs per 
        building type and returns a list where the fractions have been recovered
        into the appropriate number of jobs. These jobs are then placed into the
        categories that had the largest fractional amounts.
        
        No guarantees are made if the fractions blatently do not add up to the 
        given whole. Being off by a small amount should not alter the results, 
        however.
        """
        list = zone_building_type_and_jobs_list[:]
        building_type = 0; jobs_per_building_type = 1
        fraction = 0; index = 1; 
        
        frac_sum = 0
        whole_sum = 0
        max_frac = []
        for i in range(len(list)):
            jobs = int(list[i][jobs_per_building_type])
            whole_sum += jobs
            frac = list[i][jobs_per_building_type] - jobs
            max_frac += [(frac, i)]
            list[i] = (list[i][building_type], jobs)
        
        frac_sum = total - whole_sum

        max_frac.sort()
        max_frac.reverse()

        for i in range(frac_sum):
            next = max_frac[i]
            j = next[index]
            list[j] = (list[j][building_type], 
                       list[j][jobs_per_building_type]+1)
            
        return list
    
    
    def _zip_and_sample(self, dist, how_many):
        """
        [Internal]
        Takes a given list of 2-tuples(object, probability) and extracts a 
        sample population of objects from the list according to the 
        probabilities of the represented objects and the given sample size.
        """
        if type(dist) is not type([]):
            raise TypeError, ('Invalid input. Expected %s. Received %s.' 
                                % (type({}), type(dist)))
        
        pop = []; prob = []        
                                        
        for tuple in dist:
            if type(tuple) is not type(()):
                raise TypeError, ('Invalid input. Expected a list of %s. '
                                  'Received %s.' 
                                  % (type(()), type(tuple)))
              
            if len(tuple) != 2:
                raise TypeError, ('Invalid input. Expected tuples of length 2')
                                  
            # Don't add anything that has no chance of being chosen. This also
            # makes testing that the sum of the list is non-zero a simple length
            # check.
            if tuple[1] is not None and tuple[1] > 0:
                pop += [tuple[0]]
                prob += [tuple[1]]

        # The simple length check mentioned above. Checks that the sum of the 
        # probabilities is greater than 0.
        if len(pop) > 0:
            from decimal import Decimal
            if isinstance(prob[0], Decimal):
                prob_as_float = [float(i) for i in prob]
                return sample(pop, how_many, prob_as_float)
            return sample(pop, how_many, prob)
        else:
            return None


    def _get_building_type_proportion_by_zone(self, db, gridcells_table_name):
        """
        Queries for the regional proportion of building type by zone.
        """
        return db.GetResultsFromQuery(
            """SELECT GRID_ID, g.ZONE_ID, RESIDENTIAL_UNITS/RES_TOTAL AS RES, 
                GOVERNMENTAL_SQFT/GOV_TOTAL AS GOV, 
                COMMERCIAL_SQFT/COM_TOTAL AS COM, 
                INDUSTRIAL_SQFT/IND_TOTAL AS IND
            FROM %(grid)s AS g, 
                (SELECT ZONE_ID, 
                    SUM(RESIDENTIAL_UNITS) AS RES_TOTAL,
                    SUM(GOVERNMENTAL_SQFT) AS GOV_TOTAL,
                    SUM(COMMERCIAL_SQFT) AS COM_TOTAL,
                    SUM(INDUSTRIAL_SQFT) AS IND_TOTAL 
                FROM %(grid)s
                GROUP BY ZONE_ID) AS t
            WHERE g.ZONE_ID = t.ZONE_ID
            """ % {'grid':gridcells_table_name})


    def _create_jobs_table_data(self, dist_src, sectors, 
                                         building_types_and_ids_and_home_based):
        """
        Takes the given data and generates job table data to be output.
        """                    
        res_sample = []; jobs_table = []
        no_samples = []

        for key in sectors.keys():
            sector_num = key
            sector = sectors[key]
            for zone in sector.keys():
                for building_type, number_of_jobs in sector[zone]:
                    for type, id, home_based in building_types_and_ids_and_home_based:
                        if building_type == id: 
                            dist = dist_src[type]
                            break
                    else:
                        raise TypeError, ("Invalid building type: %s" 
                                          % building_type)
                    
                    try:
                        samples = self._zip_and_sample(dist[zone], 
                                                       int(number_of_jobs))
                        if samples is None: 
                            no_samples += [(zone, building_type)]
                            raise
                        
                    except:
                        pass
                        
                    else:
                        for type, id, home_based in building_types_and_ids_and_home_based:
                            if building_type == id and home_based == True:
                                home = 1    
                            else: home = 0                                
                        
                        for grid_id in samples:
                            jobs_table += [{'sector':sector_num, 
                                            'home':home, 
                                            'building':building_type, 
                                            'grid':grid_id}]
        
        if len(no_samples) > 0:
            print ('No job samples created for (zone, building_type): %s!' 
                   % no_samples)
        
        return jobs_table
        
        
#import os
#from opus_core.tests import opus_unittest
#from opus_core.store.mysql_database_server import MysqlDatabaseServer
#from opus_core.configurations.database_configuration import DatabaseConfiguration
#from opus_core.configuration import Configuration
#from numpy import array, ma
#
#class TestSynthesizeEmploymentData(opus_unittest.OpusTestCase):
#    # Names of databases to auto-create
#    in_db = 'synthesize_employment_data_tests_input'
#    out_db = 'synthesize_employment_data_tests_output' 
#    
#    # Names of tables to auto-create
#    gridcells = 'synthesize_employment_data_tests_gridcells'
#    gridcells_output = 'synthesize_employment_data_tests_gridcells_ouput'
#    data = 'synthesize_employment_data_tests_data'
#    jobs = 'synthesize_employment_data_tests_jobs'
#    jobs_output = 'synthesize_employment_data_tests_jobs_output'
#    
#    synthesize_employment_data_sql_setup = """
#        USE %(in_db)s;
#        
#        DROP TABLE IF EXISTS %(gridcells)s;
#        CREATE TABLE %(gridcells)s (
#            GRID_ID INT AUTO_INCREMENT, PRIMARY KEY(GRID_ID),
#            ZONE_ID INT, 
#            RESIDENTIAL_UNITS INT, COMMERCIAL_SQFT INT, INDUSTRIAL_SQFT INT, 
#                GOVERNMENTAL_SQFT INT);
#    
#        DROP TABLE IF EXISTS %(data)s;
#        CREATE TABLE %(data)s (
#            id INT AUTO_INCREMENT, PRIMARY KEY(id),
#            taz INT, ag INT, mfg INT, tcu INT, whl INT, rtl INT, fire INT, srv INT, 
#                pub INT);
#        
#        DROP TABLE IF EXISTS %(jobs)s;
#        CREATE TABLE %(jobs)s (
#            JOB_ID INT AUTO_INCREMENT, PRIMARY KEY(JOB_ID),
#            GRID_ID INT, SECTOR_ID INT, HOME_BASED TINYINT, SIC INT, 
#                IMPUTE_FLAG INT, BUILDING_TYPE INT);
#        
#        """ % {'in_db':in_db,
#               'gridcells':gridcells,
#               'data':data,
#               'jobs':jobs
#               }
#
#
#    synthesize_employment_data_sql_teardown = """
#        DROP DATABASE IF EXISTS %(in_db)s;
#        DROP DATABASE IF EXISTS %(out_db)s;
#        
#        """ % {'in_db':in_db,
#               'out_db':out_db}
#    
#    def setUp(self):
#        """
#        Create the databases that will be used in testing.
#        """
#        
#        self.config = {
#            'output_database_name':self.out_db,
#        
#            'gridcells':self.gridcells,
#            'gridcells_output':self.gridcells_output,
#            'jobs':self.jobs,
#            'jobs_by_zone_by_sector':self.data,
#            'jobs_output':self.jobs_output,
#            
#            'sector_names_and_ids':(
#                    ('ag',   1),
#                    ('mfg',  2),
#                    ('tcu',  3),
#                    ('whl',  4),
#                    ('rtl',  5),
#                    ('fire', 6),
#                    ('srv',  7),
#                    ('pub',  8)
#                ),
#                
#            'building_type_column_names_and_ids_and_home_based':(
#                    ('COM', 1, False),
#                    ('GOV', 2, False),
#                    ('IND', 3, False),
#                    ('RES', 4, True)
#                ),
#            
#            'db_config': DatabaseConfiguration(
#                host_name = 'localhost',
#                database_name = self.in_db,
#                )
#
#            'store':{
#                'drop_database_first':False,
#                },
#            }
#        
#        db_server = MysqlDatabaseServer(self.config['db_config'])
#        
#        database_name = self.config['db_config'].database_name
#        if self.config['store']['drop_database_first']:
#            db_server.drop_database(database_name)
#        db_server.create_database(database_name)
#        
#        self.input_db = db_server.get_database(database_name)
#        self.input_db.DoQueries(self.synthesize_employment_data_sql_setup)
#        
#    
#    def tearDown(self):
#        """
#        Break down the databases used in testing.
#        """
#        self.input_db.DoQueries(self.synthesize_employment_data_sql_teardown)
#        
#        self.input_db.close()
#        
#        
#    def test_zip_and_sample_input_level_1(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#        try:
#            SynthesizeJobs()._zip_and_sample('a', 1)
#            
#            self.fail("Did not fail on invalid input.")
#        except TypeError: pass
#    
#    
#    def test_zip_and_sample_input_level_2(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#        try:
#            SynthesizeJobs()._zip_and_sample(['a'], 1)
#            
#            self.fail("Did not fail on invalid input")
#        except TypeError: pass
#        
#        
#    def test_zip_and_sample_input_level_3(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#        try:
#            SynthesizeJobs()._zip_and_sample([('a','a')], 1)
#            
#            self.fail("Did not fail on invalid input")
#        except TypeError: pass
#
#
#    def test_zip_and_sample_simple_input(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#        result = SynthesizeJobs()._zip_and_sample([(2,1)], 1)
#        
#        self.assert_(str(result) == str([2]), "Unexpected output.")
#    
#        
#    def test_zip_and_sample_uneven_input_short(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#        try:
#            SynthesizeJobs()._zip_and_sample([(2,1), (2,)], 1)
#            
#            self.fail("Did not fail on invalid input.")
#        except TypeError: pass
#        
#        
#    def test_zip_and_sample_uneven_input_long(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#        try:
#            SynthesizeJobs()._zip_and_sample([(2,1), (2,1,3)], 1)
#            
#            self.fail("Did not fail on invalid input.")
#        except TypeError: pass
#        
#        
#    def test_zip_and_sample_input_none(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#
#        result = SynthesizeJobs()._zip_and_sample([(2,1), (3,None)], 1)
#        
#        self.assert_(str(result) == str([2]), "Unexpected output.")
#    
#    
#    def test_zip_and_sample_no_input(self):
#        """
#        Test that the internal method _zip_and_sample works as expected.
#        """
#        try:
#            SynthesizeJobs()._zip_and_sample(None, 1)
#            
#            self.fail("Did not fail on invalid input")
#        except TypeError: pass
#        
#        
#    def test_get_jobs_per_building_type_in_sector_by_zone(self):
#        ag_sector = 1
#        zone_val = 9
#        ag_val = 2
#        building_type = [1, 2]
#        building_types = len(building_type)
#        
#        self.input_db.execute("""
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES
#            (%(zone_val)s, %(ag_val)s, 0, 0, 0, 0, 0, 0, 0);
#            """ % {'data':self.data,
#                   'zone_val':zone_val,
#                   'ag_val':ag_val})
#       
#        self.input_db.execute("""
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED,
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (0, 0, %(ag_sector)s, 0, 0, 0, %(b1)s),
#            (0, 0, %(ag_sector)s, 0, 0, 0, %(b2)s);
#            """ % {'jobs':self.jobs,
#                   'ag_sector':ag_sector,
#                   'b1':building_type[0],
#                   'b2':building_type[1]})
#        
#        expected_output = {zone_val:[(building_type[0], ag_val/building_types),
#                                     (building_type[1], ag_val/building_types)]}
#        
#        results = (SynthesizeJobs().
#            _get_jobs_per_building_type_in_sector_by_zone(self.input_db, 
#                self.data, self.jobs, 'ag', 1))
#            
#        self.assert_(results == expected_output, 'Unexpected output. Expected '
#                    '%s. Received %s.' % (expected_output, results))
#    
#    
#    def test_get_building_type_proportion_by_zone_single_grid(self):
#        self.input_db.execute("""
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS,
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (1, 1000, 1, 1, 1, 1);
#            """ % {'grid':self.gridcells})
#        
#        expected_output = [
#                ['GRID_ID', 'ZONE_ID', 'RES', 'GOV', 'COM', 'IND'],
#                [        1,      1000,     1,     1,     1,     1]
#            ]    
#        
#        results = SynthesizeJobs()._get_building_type_proportion_by_zone(
#                                                  self.input_db, self.gridcells)
#                                                            
#        self.assert_(results == expected_output, 
#            "Unexpected output. Expected %s. Recieved %s." 
#            % (expected_output, results))
#    
#    
#    # TODO: Fix problems with Decimals & re-enable
#    #def test_get_building_type_proportion_by_zone_multiple_grids(self):
#        #self.input_db.execute("""
#            #INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS,
#                #GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            #(1, 1000, 1, 0, 1, 2),
#            #(2, 1000, 1, 1, 0, 3),
#            #(3, 1000, 0, 1, 1, 5);
#            #""" % {'grid':self.gridcells})
#                
#        #expected_output = [
#            #['GRID_ID', 'ZONE_ID', 'RES', 'GOV', 'COM', 'IND'],
#            #array([        1,      1000,   0.5,     0,   0.5,   0.2]),
#            #array([        2,      1000,   0.5,   0.5,     0,   0.3]),
#            #array([        3,      1000,     0,   0.5,   0.5,   0.5]),
#            #]
#        
#        #results = SynthesizeJobs()._get_building_type_proportion_by_zone(
#                                                  #self.input_db, self.gridcells)
#                                                            
#        #self.assert_(results[0] == expected_output[0], 
#            #"Unexpected output. Expected %s. Recieved %s" 
#            #% (expected_output, results))
#        #for i in range(1, len(results)):
#            #self.assert_(ma.allclose(results[i], expected_output[i]), 
#                #"Unexpected output. Expected %s. Recieved %s" 
#                #% (expected_output, results))
#            
#     
#    # TODO: Fix problems with Decimals & re-enable
#    #def test_get_building_type_proportion_by_zone_multiple_zones(self):
#        #self.input_db.execute("""
#            #INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS,
#                #GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            #(1, 1000, 1, 0, 1, 2),
#            #(2, 1000, 1, 1, 0, 3),
#            #(3, 1000, 0, 1, 1, 5),
#            
#            #(4, 2000, 10,  2, 25, 2),
#            #(5, 2000, 15, 50, 25, 3),
#            #(6, 2000, 75, 48, 50, 5);
#            #""" % {'grid':self.gridcells})
#                
#        #expected_output = [
#            #['GRID_ID', 'ZONE_ID', 'RES', 'GOV', 'COM', 'IND'],
#            #array([        1,      1000,   0.5,     0,   0.5,   0.2]),
#            #array([        2,      1000,   0.5,   0.5,     0,   0.3]),
#            #array([        3,      1000,     0,   0.5,   0.5,   0.5]),
#            #array([        4,      2000,   0.1,  0.02,  0.25,   0.2]),
#            #array([        5,      2000,  0.15,   0.5,  0.25,   0.3]),
#            #array([        6,      2000,  0.75,  0.48,   0.5,   0.5]),
#            #]
#        
#        #results = SynthesizeJobs()._get_building_type_proportion_by_zone(
#                                                  #self.input_db, self.gridcells)
#                                                            
#        #self.assert_(results[0] == expected_output[0], 
#            #"Unexpected output. Expected %s. Recieved %s" 
#            #% (expected_output, results))
#        #for i in range(1, len(results)):
#            #self.assert_(ma.allclose(results[i], expected_output[i]), 
#                #"Unexpected output. Expected %s. Recieved %s" 
#                #% (expected_output, results))
#            
#    
#    def test_resolve_fractional_jobs_single_clean(self):
#        input = [(1,1.2), (2,1.4), (3,1.3), (4,1.1)]
#        expected_output = [(1,1), (2,2), (3,1), (4,1)]
#        
#        results = SynthesizeJobs()._resolve_fractional_jobs(input, 5)
#       
#        self.assert_(results == expected_output,
#            'Unexpected output. Expected %s. Recieved %s.'
#            % (expected_output, results))
#    
#    
#    def test_resolve_fractional_jobs_single_dirty(self):
#        input = [(1,1.1999), (2,1.3999), (3,1.2999), (4,1.0999)]
#        expected_output = [(1,1), (2,2), (3,1), (4,1)]
#        
#        results = SynthesizeJobs()._resolve_fractional_jobs(input, 5)
#       
#        self.assert_(results == expected_output,
#            'Unexpected output. Expected %s. Recieved %s.'
#            % (expected_output, results))
#            
#            
#    def test_resolve_fractional_jobs_multiple_clean(self):
#        input = [(1,1.9), (2,1.7), (3,1.6), (4,1.8)]
#        expected_output = [(1,2), (2,2), (3,1), (4,2)]
#        
#        results = SynthesizeJobs()._resolve_fractional_jobs(input, 7)
#       
#        self.assert_(results == expected_output,
#            'Unexpected output. Expected %s. Recieved %s.'
#            % (expected_output, results))
#    
#    
#    def test_resolve_fractional_jobs_multiple_dirty(self):
#        input = [(1,1.8999), (2,1.6999), (3,1.5999), (4,1.7999)]
#        expected_output = [(1,2), (2,2), (3,1), (4,2)]
#        
#        results = SynthesizeJobs()._resolve_fractional_jobs(input, 7)
#       
#        self.assert_(results == expected_output,
#            'Unexpected output. Expected %s. Recieved %s.'
#            % (expected_output, results))
#                
#    
#    def test_create_jobs_table_data_simple(self):
#        dist = {}
#        dist['COM'] = {'zone':[(1000,1)]}
#        dist['GOV'] = dist['IND'] = dist['RES'] = {}
#        
#        sector = {}
#        
#        sector[1] = {'zone':[(1,1)]}
#
#        for i in range(2, 9):
#            sector[i] = {}
#        
#        expected_output = [{'sector':1,
#                            'home':0,
#                            'grid':1000,
#                            'building':1}]
#                            
#        building_types_and_home_based = self.config[
#                            'building_type_column_names_and_ids_and_home_based']
#        
#        results = SynthesizeJobs()._create_jobs_table_data(dist, sector,
#                                                  building_types_and_home_based)
#            
#        self.assert_(results == expected_output,
#                     'Unexpected output. Expected %s. Recieved %s.'
#                     % (expected_output, results))
#            
#            
#    def test_create_jobs_table_data_multiple_zones_per_sector(self):
#        dist = {}
#        dist['COM'] = {'zone':[(1000,1)],
#                    'zone1':[(2000,1)]}
#        dist['GOV'] = dist['IND'] = dist['RES'] = {}
#        
#        sector = {}
#        sector[1] = {'zone':[(1,1)],
#              'zone1':[(1,1)]}
#      
#        building_types_and_home_based = self.config[
#                            'building_type_column_names_and_ids_and_home_based']
#      
#        for i in range(2,9):
#            sector[i] = {}
#        
#        # We don't know in which order the dictionary will hash the zones, so
#        # there is more than one possible output.
#        possible_output1 = [
#            {'sector':1, 'home':0, 'grid':1000, 'building':1},
#            {'sector':1, 'home':0, 'grid':2000, 'building':1},
#            ]
#        
#        possible_output2 = [
#            {'sector':1, 'home':0, 'grid':2000, 'building':1},
#            {'sector':1, 'home':0, 'grid':1000, 'building':1},
#            ]
#        
#        results = SynthesizeJobs()._create_jobs_table_data(dist, sector,
#                                                  building_types_and_home_based)
#            
#        try:
#            self.assert_(results == possible_output2,
#                         'Unexpected output. Expected %s or %s. Recieved %s.'
#                         % (possible_output1, possible_output2, results))                        
#            
#        except AssertionError:
#            self.assert_(results == possible_output1,
#                         'Unexpected output. Expected %s or %s. Recieved %s.'
#                         % (possible_output1, possible_output2, results))
#
#            
#                     
#            
#    def test_create_jobs_table_data_complex(self):
#        dist = {}
#        dist['COM'] = {'zone':[(1000,1), (2000,0), (3000,0), (4000,0)],
#                    'zone2':[(5000,0), (6000,0), (7000,0), (8000,1)]}
#                    
#        dist['GOV'] = {'zone':[(1000,0), (2000,1), (3000,0), (4000,0)],
#                    'zone2':[(5000,1), (6000,0), (7000,0), (8000,0)]}
#                    
#        dist['IND'] = {'zone':[(1000,0), (2000,0), (3000,1), (4000,0)],
#                    'zone2':[(5000,0), (6000,1), (7000,0), (8000,0)]}
#                    
#        dist['RES'] = {'zone3':[(9000,0), (10000,0), (11000,1), (12000,0)]}
#        
#        sector = {}
#        
#        sector[1] = {'zone':[(1,1), (2,1), (3,1), (4,0)]}
#        
#        sector[2] = {'zone3':[(1,1), (2,1), (3,0), (4,1)]}
#        
#        sector[3] = {'zone':[(1,1), (2,0), (3,1), (4,1)]}
#        
#        sector[4] = {'zone':[(1,0), (2,1), (3,1), (4,1)]}
#        
#        sector[5] = {'zone':[(1,1), (2,1), (3,0), (4,0)]}
#        
#        sector[6] = {'zone3':[(1,0), (2,0), (3,1), (4,1)]}
#                
#        sector[7] = {'zone3':[(1,0), (2,1), (3,0), (4,0)]}
#               
#        sector[8] = {'zone2':[(1,0), (2,0), (3,0), (4,1)]}
#        
#        building_types_and_home_based = self.config[
#                            'building_type_column_names_and_ids_and_home_based']
#        
#        expected_output = [
#            {'sector':1,'home':0,'grid':1000,'building':1},
#            {'sector':1,'home':0,'grid':2000,'building':2},
#            {'sector':1,'home':0,'grid':3000,'building':3},
#            {'sector':2,'home':1,'grid':11000,'building':4},
#            {'sector':3,'home':0,'grid':1000,'building':1},
#            {'sector':3,'home':0,'grid':3000,'building':3},
#            {'sector':4,'home':0,'grid':2000,'building':2},
#            {'sector':4,'home':0,'grid':3000,'building':3},
#            {'sector':5,'home':0,'grid':1000,'building':1},
#            {'sector':5,'home':0,'grid':2000,'building':2},
#            {'sector':6,'home':1,'grid':11000,'building':4}
#            ]
#            
#        results = SynthesizeJobs()._create_jobs_table_data(dist, sector,
#                                                  building_types_and_home_based)
#            
#        self.assert_(results == expected_output,
#                     'Unexpected output. Expected %s. Received %s.'
#                     % (expected_output, results))
#    
#    
#    def test_setup_databases(self):
#        """
#        Test that the setUp databases were created, as expected.
#        """
#
#        results = self.input_db.GetResultsFromQuery('SHOW DATABASES;')
#        self.assert_([self.in_db] in results, 'Database %s not created.' 
#                                              % self.in_db)
#       
#                
#    def test_setup_tables(self):
#        """
#        Test that the setUp tables were created, as expected.
#        """
#        
#        try:
#            results = self.input_db.GetResultsFromQuery("""
#                SELECT COUNT(*) FROM $$.%(data)s
#            """ % {'data':self.data})
#        except: self.fail('Table %s not created.' % self.data)
#                
#        try:
#            results = self.input_db.GetResultsFromQuery("""
#                SELECT COUNT(*) FROM $$.%(jobs)s
#            """ % {'jobs':self.jobs})
#            
#        except: self.fail('Table %s not created.' % self.jobs)
#
#    
#    def test_synchronize_employment_data_output_exists(self):
#        """
#        Test that the correct output database is created.
#        """
#        self.input_db.execute("""
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES
#            (1, 2, 3, 4, 5, 6, 7, 8, 9);
#            """ % {'data':self.data})
#       
#        self.input_db.execute("""
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED,
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (1, 2, 3, 4, 5, 6, 1);
#            """ % {'jobs':self.jobs})
#       
#        self.input_db.execute("""
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS,
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (2, 1, 3, 4, 5, 6);
#            """ % {'grid':self.gridcells})
#    
#        SynthesizeJobs().synthesize_employment_data(self.config)
#    
#        try:
#            self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#        except: self.fail('Database %s was not created.' % self.out_db)
#       
#       
#    def test_synchronize_employment_data_output_jobs_table_exists(self):
#        """
#        Test that the output table exists, as expected.
#        """
#        self.input_db.execute("""
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES
#            (1, 1, 2, 2, 2, 2, 2, 2, 2);
#            """ % {'data':self.data})
#       
#        self.input_db.execute("""
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED,
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (1, 1, 1, 0, 0, 0, 1);
#            """ % {'jobs':self.jobs})
#       
#        self.input_db.execute("""
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, COMMERCIAL_SQFT,
#                GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT, RESIDENTIAL_UNITS) VALUES
#            (1, 1, 1, 0, 0, 0);
#            """ % {'grid':self.gridcells})
#    
#        SynthesizeJobs().synthesize_employment_data(self.config)
#    
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#        
#        try:
#            results = self.input_db.GetResultsFromQuery("""
#                SELECT * FROM %(jobs_out)s
#                """ % {'jobs_out':self.jobs_output})
#
#        except:
#            self.fail('Output table %s does not exist.' % self.jobs_output)
#            
#            
##    def test_synchronize_employment_data_output_gridcells_table_exists(self):
##        """
##        Test that the output table exists, as expected.
##        """
##        self.input_db.execute("""
##            INSERT INTO $$.%(data)s 
##                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES
##            (1, 1, 1, 1, 1, 1, 1, 1, 1);
##            """ % {'data':self.data})
##       
##        self.input_db.execute("""
##            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED,
##                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
##            (1, 1, 1, 0, 0, 0, 1);
##            """ % {'jobs':self.jobs})
##       
##        self.input_db.execute("""
##            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS,
##                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
##            (1, 1, 1, 0, 0, 0);
##            """ % {'grid':self.gridcells})
##    
##        SynthesizeJobs().synthesize_employment_data(self.config)
##    
##        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
##        
##        try:
##            results = self.input_db.GetResultsFromQuery("""
##                SELECT * FROM %(grid_out)s
##                """ % {'grid_out':self.gridcells_output})
##                
##        except:
##            self.fail('Output table %s does not exist.' % self.gridcells_output)
#            
#            
#    def test_synchronize_employment_data_output_jobs_is_correct(self):
#        """
#        Test that the correct data is in the output table.
#        """
#        
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    0,    0,    0,    0,      0,    0,    0,     1   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    8,     0,    0,    0,    3    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    0,    0,    0,    1    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        expected_output = [
#            ['JOB_ID', 'GRID_ID', 'HOME_BASED', 'SECTOR_ID', 'BUILDING_TYPE'],
#            array([       1,      1000,            0,           8,               3])
#            ]
#    
#        SynthesizeJobs().synthesize_employment_data(self.config)
#    
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#        
#        results = self.input_db.GetResultsFromQuery("""
#            SELECT * FROM %(jobs_out)s
#            """ % {'jobs_out':self.jobs_output})
#        
#        self.assert_(results[0] == expected_output[0], 
#            "Unexpected output. Expected %s. Recieved %s" 
#            % (expected_output, results))
#        self.assert_(ma.allclose(results[1:], expected_output[1:]), 
#            "Unexpected output. Expected %s. Recieved %s" 
#            % (expected_output, results))
#            
#            
##    def test_synchronize_employment_data_output_gridcells_is_correct_simple(self):
##        """
##        Test that the correct data is in the output table.
##        """
##        
##        insert_data_query = """
##            INSERT INTO $$.%(data)s 
##                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
##            (    100,    0,    0,    0,    0,      0,    0,    0,     1   );
##            """ % {'data':self.data}
##        self.input_db.execute(insert_data_query)
##        
##        insert_job_query = """
##            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
##                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
##            (    1,     1000,    8,     0,    0,    0,    3    );
##            """ % {'jobs':self.jobs}
##        self.input_db.execute(insert_job_query)
##        
##        insert_gridcell_query = """
##            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, COMMERCIAL_SQFT, 
##                GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT, RESIDENTIAL_UNITS) VALUES
##            (    1000,    100,    0,    0,    1,    0    );
##            """ % {'grid':self.gridcells}
##        self.input_db.execute(insert_gridcell_query)
##        
##        expected_output = [
##            ['GRID_ID', 'ZONE_ID', 'RESIDENTIAL_UNITS', 'COMMERCIAL_SQFT', 
##                                        'INDUSTRIAL_SQFT', 'GOVERNMENTAL_SQFT'],
##            [     1000,       100,                   0,                 0,                                                       
##                                                        1,                   0]
##            ]
##    
##        SynthesizeJobs().synthesize_employment_data(self.config)
##    
##        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
##        
##        results = self.input_db.GetResultsFromQuery("""
##            SELECT * FROM %(grid_out)s
##            """ % {'grid_out':self.gridcells_output})
##        
##        self.assert_(results == expected_output, 
##            "Unexpected output. Expected %s. Recieved %s" 
##            % (expected_output, results))
#            
#
##    def test_synchronize_employment_data_output_gridcells_is_correct_complex(self):
##        """
##        Test that the correct data is in the output table.
##        """
##        
##        insert_data_query = """
##            INSERT INTO $$.%(data)s 
##                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
##            (    100,    0,    0,    0,    0,      0,    0,    0,     1   );
##            """ % {'data':self.data}
##        self.input_db.execute(insert_data_query)
##        
##        insert_job_query = """
##            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
##                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
##            (    1,     1000,    8,     0,    0,    0,    3    );
##            """ % {'jobs':self.jobs}
##        self.input_db.execute(insert_job_query)
##        
##        insert_gridcell_query = """
##            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, COMMERCIAL_SQFT, 
##                GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT, RESIDENTIAL_UNITS) VALUES
##            (    1000,    100,    0,    0,    1,    0    );
##            """ % {'grid':self.gridcells}
##        self.input_db.execute(insert_gridcell_query)
##        
##        expected_output = [
##            ['GRID_ID', 'ZONE_ID', 'RESIDENTIAL_UNITS', 'COMMERCIAL_SQFT', 
##                                        'INDUSTRIAL_SQFT', 'GOVERNMENTAL_SQFT'],
##            [     1000,       100,                   0,                 0,                                                       
##                                                        1,                   0]
##            ]
##    
##        SynthesizeJobs().synthesize_employment_data(self.config)
##    
##        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
##        
##        results = self.input_db.GetResultsFromQuery("""
##            SELECT * FROM %(grid_out)s
##            """ % {'grid_out':self.gridcells_output})
##        
##        self.assert_(results == expected_output, 
##            "Unexpected output. Expected %s. Recieved %s" 
##            % (expected_output, results))
#        
#        
#    def test_synchronize_employment_data_empty_input(self):
#        """
#        Test that the method responds correctly to empty input tables.
#        """
#        try:
#            SynthesizeJobs().synthesize_employment_data(self.config)
#            
#            self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            results = self.input_db.GetResultsFromQuery(
#                'SELECT COUNT(*) FROM %(jobs_out)s' 
#                % {'jobs_out':self.jobs_output})
#                
#            self.assert_(results[1] == [0], 'Output table is not empty!')
#            
#        except Exception, val: 
#            self.fail('Method synchronize_employment_data() failed on empty ' + 
#                      'input. (%s: %s)' % (Exception, val))
#  
#
#    def test_synchronize_employment_data_no_jobs(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    0,    0,    0,    0,      0,    0,    0,     0   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        expected_output = [0]
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    1,    1,    1,    1    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        get_job_results = (
#            'SELECT COUNT(*) FROM %(jobs_out)s' % {'jobs_out':self.jobs_output})
#        
#        results = self.input_db.GetResultsFromQuery(get_job_results)
#        
#        self.assert_(results[1] == expected_output, 
#            'Unexpected output. Expected %s. Received %s.' 
#            % (expected_output, results[1]))
#                   
#                   
#    def test_synchronize_employment_data_simple(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    5,    3,    3,    3,      3,    3,    3,     3   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        expected_output = array([5])
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    1,    1,    1,    2    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        get_job_results = (
#            'SELECT COUNT(*) FROM %(jobs_out)s' % {'jobs_out':self.jobs_output})
#        
#        results = self.input_db.GetResultsFromQuery(get_job_results)
#        
#        self.assert_(ma.allclose(results[1], expected_output), 
#            'Unexpected output. Expected %s. Received %s.' 
#            % (expected_output, results[1]))
#        
#        
#    def test_synchronize_employment_data_simple_all(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    8,    16,    20,     24,    28,    32,    36   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        expected_output = array([4+8+16+20+24+28+32+36])
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    2,     0,    0,    0,    1    ),
#            (    3,     1000,    3,     0,    0,    0,    1    ),
#            (    4,     1000,    4,     0,    0,    0,    1    ),
#            (    5,     1000,    5,     0,    0,    0,    1    ),
#            (    6,     1000,    6,     0,    0,    0,    1    ),
#            (    7,     1000,    7,     0,    0,    0,    1    ),
#            (    8,     1000,    8,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    1,    1,    1,    1    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        get_job_results = (
#            'SELECT COUNT(*) FROM %(jobs_out)s' % {'jobs_out':self.jobs_output})
#        
#        results = self.input_db.GetResultsFromQuery(get_job_results)
#        
#        self.assert_(ma.allclose(results[1], expected_output), 
#            'Unexpected output. Expected %s. Received %s.' 
#            % (expected_output, results[1]))
#            
#            
#    def test_synchronize_employment_data_simple_all_but_one(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    8,    16,    20,     24,   999,    32,    36   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        expected_output = array([4+8+16+20+24+0+32+36])
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    2,     0,    0,    0,    1    ),
#            (    3,     1000,    3,     0,    0,    0,    1    ),
#            (    4,     1000,    4,     0,    0,    0,    1    ),
#            (    5,     1000,    5,     0,    0,    0,    1    ),
#            (    7,     1000,    7,     0,    0,    0,    1    ),
#            (    8,     1000,    8,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    1,    1,    1,    1    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        get_job_results = (
#            'SELECT COUNT(*) FROM %(jobs_out)s' % {'jobs_out':self.jobs_output})
#        
#        results = self.input_db.GetResultsFromQuery(get_job_results)
#        
#        self.assert_(ma.allclose(results[1], expected_output), 
#            'Unexpected output. Expected %s. Received %s.' 
#            % (expected_output, results[1]))
#            
#
#    def test_synchronize_employment_data_simple_more_grids(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    8,    12,    16,    20,   24,    28,    32   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        expected_output = array([4+8+12+16+20+24+28+32])
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    2,     0,    0,    0,    1    ),
#            (    3,     1000,    3,     0,    0,    0,    1    ),
#            (    4,     1000,    4,     0,    0,    0,    1    ),
#            (    5,     2000,    5,     0,    0,    0,    1    ),
#            (    6,     2000,    6,     0,    0,    0,    1    ),
#            (    7,     2000,    7,     0,    0,    0,    1    ),
#            (    8,     2000,    8,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    1,    1,    1,    1    ),
#            (    2000,    100,    1,    1,    1,    1    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        get_job_results = (
#            'SELECT COUNT(*) FROM %(jobs_out)s' % {'jobs_out':self.jobs_output})
#        
#        results = self.input_db.GetResultsFromQuery(get_job_results)
#        
#        self.assert_(ma.allclose(results[1], expected_output), 
#            'Unexpected output. Expected %s. Received %s.' 
#            % (expected_output, results[1]))
#
#
#    def test_synchronize_employment_data_simple_evenly_divisible(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    0,    0,    0,    0,   0,    0,    0   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        expected_output = array([4+0+0+0+0+0+0+0])
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    1,     0,    0,    0,    2    ),
#            (    3,     1000,    1,     0,    0,    0,    3    ),
#            (    4,     1000,    1,     0,    0,    0,    4    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    1,    1,    1,    1    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        get_job_results = (
#            'SELECT COUNT(*) FROM %(jobs_out)s' % {'jobs_out':self.jobs_output})
#        
#        results = self.input_db.GetResultsFromQuery(get_job_results)
#        
#        self.assert_(ma.allclose(results[1], expected_output), 
#            'Unexpected output. Expected %s. Received %s.' 
#            % (expected_output, results[1]))
#            
#
#    def test_synchronize_employment_data_simple_unevenly_divisible(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    2,    0,    0,    0,    0,   0,    0,    0   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        expected_output = array([2+0+0+0+0+0+0+0])
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    1,     0,    0,    0,    2    ),
#            (    3,     1000,    1,     0,    0,    0,    3    ),
#            (    4,     1000,    1,     0,    0,    0,    4    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    1,    1,    1,    1    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        get_job_results = (
#            'SELECT COUNT(*) FROM %(jobs_out)s' % {'jobs_out':self.jobs_output})
#        
#        results = self.input_db.GetResultsFromQuery(get_job_results)
#        
#        self.assert_(ma.allclose(results[1], expected_output), 
#            'Unexpected output. Expected %s. Received %s.' 
#            % (expected_output, results[1]))
#      
#            
#    def test_no_more_residential_jobs_than_available_units(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    8,    12,    16,    20,   24,    28,    32   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    2,     0,    0,    0,    1    ),
#            (    3,     1000,    3,     0,    0,    0,    1    ),
#            (    4,     1000,    4,     0,    0,    0,    1    ),
#            (    5,     2000,    5,     0,    0,    0,    1    ),
#            (    6,     2000,    6,     0,    0,    0,    1    ),
#            (    7,     2000,    7,     0,    0,    0,    1    ),
#            (    8,     2000,    8,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    100,    100,    100,    100    ),
#            (    2000,    100,    100,    100,    100,    100    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        query = ("""
#            select * from
#                (SELECT g.grid_id, 
#                    count(j.job_id) num_jobs, 
#                    sum(g.residential_units) num_units
#                FROM %(out_db)s.%(jobs_out)s j,
#                    $$.%(grid)s g
#                where j.grid_id = g.grid_id
#                    and j.home_based = 1
#                group by g.grid_id) as t
#            where num_jobs > num_units
#            """ % {
#               'out_db':self.out_db,
#               'jobs_out':self.jobs_output,
#               'grid':self.gridcells
#               })
#        
#        results = self.input_db.GetResultsFromQuery(query)
#        
#        self.assert_(len(results[1:]) == 0, 
#            'Unexpected output. Expected no results. Received %s.' 
#            % results[1:])
#            
#    
#    def test_commercial_jobs_have_available_sqft(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    8,    12,    16,    20,   24,    28,    32   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    2,     0,    0,    0,    1    ),
#            (    3,     1000,    3,     0,    0,    0,    1    ),
#            (    4,     1000,    4,     0,    0,    0,    1    ),
#            (    5,     2000,    5,     0,    0,    0,    1    ),
#            (    6,     2000,    6,     0,    0,    0,    1    ),
#            (    7,     2000,    7,     0,    0,    0,    1    ),
#            (    8,     2000,    8,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    100,    100,    100,    100    ),
#            (    2000,    100,    100,    100,    100,    100    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        query = ("""
#            select * from (
#                SELECT g.grid_id, 
#                    sum(commercial_sqft) / count(j.job_id) sqft_per_job
#                FROM %(out_db)s.%(jobs_out)s j,
#                    $$.%(grid)s g
#                where j.grid_id = g.grid_id
#                    and j.building_type = 1
#                group by g.grid_id) as t
#            where sqft_per_job < 100
#            """ % {
#               'out_db':self.out_db,
#               'jobs_out':self.jobs_output,
#               'grid':self.gridcells
#               })
#        
#        results = self.input_db.GetResultsFromQuery(query)
#        
#        self.assert_(len(results[1:]) == 0, 
#            'Unexpected output. Expected no results. Received %s.' 
#            % results[1:])
#            
#            
#    def test_industrial_jobs_have_available_sqft(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    8,    12,    16,    20,   24,    28,    32   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    2,     0,    0,    0,    1    ),
#            (    3,     1000,    3,     0,    0,    0,    1    ),
#            (    4,     1000,    4,     0,    0,    0,    1    ),
#            (    5,     2000,    5,     0,    0,    0,    1    ),
#            (    6,     2000,    6,     0,    0,    0,    1    ),
#            (    7,     2000,    7,     0,    0,    0,    1    ),
#            (    8,     2000,    8,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    100,    100,    100,    100    ),
#            (    2000,    100,    100,    100,    100,    100    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        query = ("""
#            select * from (
#                SELECT g.grid_id, 
#                    sum(industrial_sqft) / count(j.job_id) sqft_per_job
#                FROM %(out_db)s.%(jobs_out)s j,
#                    $$.%(grid)s g
#                where j.grid_id = g.grid_id
#                    and j.building_type = 3
#                group by g.grid_id) as t
#            where sqft_per_job < 100
#            """ % {
#               'out_db':self.out_db,
#               'jobs_out':self.jobs_output,
#               'grid':self.gridcells
#               })
#        
#        results = self.input_db.GetResultsFromQuery(query)
#        
#        self.assert_(len(results[1:]) == 0, 
#            'Unexpected output. Expected no results. Received %s.' 
#            % results[1:])
#            
#            
#    def test_governmental_jobs_have_available_sqft(self):
#        insert_data_query = """
#            INSERT INTO $$.%(data)s 
#                (taz, ag, mfg, tcu, whl, rtl, fire, srv, pub) VALUES 
#            (    100,    4,    8,    12,    16,    20,   24,    28,    32   );
#            """ % {'data':self.data}
#        self.input_db.execute(insert_data_query)
#        
#        insert_job_query = """
#            INSERT INTO $$.%(jobs)s (JOB_ID, GRID_ID, SECTOR_ID, HOME_BASED, 
#                SIC, IMPUTE_FLAG, BUILDING_TYPE) VALUES
#            (    1,     1000,    1,     0,    0,    0,    1    ),
#            (    2,     1000,    2,     0,    0,    0,    1    ),
#            (    3,     1000,    3,     0,    0,    0,    1    ),
#            (    4,     1000,    4,     0,    0,    0,    1    ),
#            (    5,     2000,    5,     0,    0,    0,    1    ),
#            (    6,     2000,    6,     0,    0,    0,    1    ),
#            (    7,     2000,    7,     0,    0,    0,    1    ),
#            (    8,     2000,    8,     0,    0,    0,    1    );
#            """ % {'jobs':self.jobs}
#        self.input_db.execute(insert_job_query)
#        
#        insert_gridcell_query = """
#            INSERT INTO $$.%(grid)s (GRID_ID, ZONE_ID, RESIDENTIAL_UNITS, 
#                GOVERNMENTAL_SQFT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT) VALUES
#            (    1000,    100,    100,    100,    100,    100    ),
#            (    2000,    100,    100,    100,    100,    100    );
#            """ % {'grid':self.gridcells}
#        self.input_db.execute(insert_gridcell_query)
#        
#        SynthesizeJobs().synthesize_employment_data(self.config)
#        
#        self.input_db.execute('USE %(out)s' % {'out':self.out_db})
#            
#        query = ("""
#            select * from (
#                SELECT g.grid_id, 
#                    sum(governmental_sqft) / count(j.job_id) sqft_per_job
#                FROM %(out_db)s.%(jobs_out)s j,
#                    $$.%(grid)s g
#                where j.grid_id = g.grid_id
#                    and j.building_type = 2
#                group by g.grid_id) as t
#            where sqft_per_job < 100
#            """ % {
#               'out_db':self.out_db,
#               'jobs_out':self.jobs_output,
#               'grid':self.gridcells
#               })
#        
#        results = self.input_db.GetResultsFromQuery(query)
#        
#        self.assert_(len(results[1:]) == 0, 
#            'Unexpected output. Expected no results. Received %s.' 
#            % results[1:])
#        
#        
#            
#        
#if __name__ == '__main__':            
#    opus_unittest.main()