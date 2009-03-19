# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.session_configuration import SessionConfiguration
        
from opus_core.tests import opus_unittest
from numpy import array, arange, allclose
import tempfile, os, shutil, sys
from glob import glob
import urbansim.tools.do_refinement

class TestDoingRefinement(opus_unittest.OpusTestCase):
    script = urbansim.tools.do_refinement.__file__
    
    def setUp(self):
        self.urbansim_tmp = tempfile.mkdtemp(prefix='urbansim_tmp')

    def tearDown(self):
        shutil.rmtree(self.urbansim_tmp)

    def prepare_cache(self, up_to_year=None):
        self.cache_dir = os.path.join(self.urbansim_tmp, 'urbansim_cache')

        data = {
            2000:{
                'refinements' : {
                    'refinement_id': arange(1, 8),
                    'year':          array([2021,2021,2021,2022, 2023, 2027, 2027]),
                    'transaction_id':array([1,      1,   1,   2,    3,    1,    1]),
                    'action':        array(['subtract', 'subtract', 'add', 'target', 'add', 'add', 'set_value']),
                    'amount':        array([2,      1,   4,   7,    1,      1,    -1]),
                    'agent_dataset': array(['job',
                                            'job',
                                            'job',
                                            'household',
                                            '',
                                            'household',
                                            'person'
                                            ]),
                    'agent_expression': array(['job.sector_id==13',
                                               'job.sector_id==13',
                                               '',
                                               'household.household_id>0',
                                               'household.persons>5',
                                               'household.persons==3',
                                               'person.job_id'
                                              ]),
                    'location_expression': array(['building.disaggregate(parcel.raz_id)==3',
                                                  'building.disaggregate(parcel.raz_id)==4',
                                                  '(building.disaggregate(parcel.raz_id)==5) * (building.disaggregate(parcel.generic_land_use_type_id)==4)',
                                                  'building.disaggregate(parcel.raz_id)==6',
                                                  'building.disaggregate(parcel.raz_id)==6',
                                                  'building.disaggregate(parcel.raz_id)==6',
                                                  'household.refinement_id==6'
                                                  ]),
                    'location_capacity_attribute':array(['',
                                                         'non_residential_sqft',
                                                         'non_residential_sqft',
                                                         'residential_units',
                                                         'residential_units',
                                                         '',
                                                         ''
                                                      ])
                    },
                },
            2020:{
                'buildings': {
                    'building_id': array([1, 2, 3, 4, 5, 6, 7, 8]),
                    'parcel_id':   array([1, 2, 2, 3, 4, 4, 5, 5]),
                    'non_residential_sqft': \
                                   array([6, 2, 3, 6, 1, 2, 5, 0]),
                    'residential_units': \
                                   array([0, 0, 0, 0, 0, 0, 1, 1])
                },
                'parcels': {
                    'parcel_id':                array([1, 2, 3, 4, 5]),
                    'generic_land_use_type_id': array([6, 6, 3, 4, 1]),
                    'raz_id':                   array([3, 4, 5, 5, 6])
                    },
                'jobs': {
                    'job_id':      array([ 1, 2, 3, 4, 5, 6, 7, 8]),
                    'building_id': array([ 1, 1, 2, 3, 6, 1, 6, 4]),
                    'sector_id':   array([13,12,13,12,13,13,12,13]),
                    'dummy_id':    array([ 1, 2, 3, 4, 5, 6, 7, 8])
                    },
                },
        
            2022:{
                'households': {
                    'household_id': array([1, 2]),
                    'building_id':  array([7, 8]),
                    'persons':      array([3, 4]),
                    },
                'persons' : {
                    'person_id':    array([ 1,  2,  3,  4,  5,  6,  7]),
                    'household_id': array([ 1,  1,  1,  2,  2,  2,  2]),
                    'job_id':       array([ 2,  1, -1, -1,  3,  4,  7])
                    },
            },
            2023:{
                'households': {
                    'household_id': array([1, 2]),
                    'building_id':  array([7, 8]),
                    'persons':      array([3, 4]),
                    },
                'persons' : {
                    'person_id':    array([ 1,  2,  3,  4,  5,  6,  7]),
                    'household_id': array([ 1,  1,  1,  2,  2,  2,  2]),
                    'job_id':       array([ 2,  1, -1, -1,  3,  4,  7])
                    },
            },
            2027:{
                'households': {
                    'household_id': array([1, 2]),
                    'building_id':  array([7, 8]),
                    'persons':      array([3, 4]),
                    },
                'persons' : {
                    'person_id':    array([ 1,  2,  3,  4,  5,  6,  7]),
                    'household_id': array([ 1,  1,  1,  2,  2,  2,  2]),
                    'job_id':       array([ 2,  1, -1, -1,  3,  4,  7])
                    },
            },
        }
        
        self.write_datasets_to_cache(data, up_to_year=up_to_year)
        SimulationState().set_cache_directory(self.cache_dir)
        attribute_cache = AttributeCache()
        self.dataset_pool = SessionConfiguration(new_instance=True,
                                                 package_order=['urbansim', 'opus_core'],
                                                 in_storage=attribute_cache).get_dataset_pool()
        
        
    def write_datasets_to_cache(self, datasets_by_year, up_to_year=None):
        """Write datasets by year to cache"""
        for year, datasets in datasets_by_year.iteritems():
            if up_to_year is not None and year > up_to_year: continue
            SimulationState().set_current_time(year)
            year_dir = os.path.join(self.cache_dir, str(year))
            flt_storage = StorageFactory().get_storage('flt_storage', storage_location=year_dir)
            for table_name, data in datasets.iteritems():
                flt_storage.write_table(table_name, data)

    def test_do_nothing_if_no_refinements_specified_between_start_year_and_end_year(self):
        self.prepare_cache(2000)
        os.system("%(python)s  %(script)s -c %(cache_directory)s -s %(start_year)s -e %(end_year)s" % 
                  {'python': sys.executable, 'script': self.script, 'cache_directory':self.cache_dir,
                   'start_year': 2005, 'end_year': 2010 }
                  )

        dir_names = glob(os.path.join(self.cache_dir, '*'))
        expected_dir_names = [ os.path.join(self.cache_dir, '2000') ]
        
        self.assert_(set(dir_names).issubset(set(expected_dir_names)))
        self.assertEqual(set(dir_names).symmetric_difference(set(expected_dir_names)), set([]))
        
        #expected_dataset_names = []
        #for year_dir in expected_dir_names:
            #dataset_names = [ os.path.basename(p) for p in glob(os.path.join(year_dir, '*'))]
            #self.assert_( set(dataset_names).issubset( set(expected_dataset_names) ) )
            #self.assertEqual(set(dataset_names).symmetric_difference( set(expected_dataset_names) ), set(['refinements']) )

    def test_backup(self):
        self.prepare_cache()
        os.system("%(python)s  %(script)s -c %(cache_directory)s -s %(start_year)s -e %(end_year)s --backup-before-refinement" % 
                  {'python': sys.executable, 'script': self.script, 'cache_directory':self.cache_dir,
                   'start_year': 2020, 'end_year': 2020 }
                  )
        backup_dir = os.path.join(self.cache_dir, "backup", "2020")
        self.assert_(os.path.exists(backup_dir))
        
        expected_dataset_names = [ os.path.basename(p) for p in glob( os.path.join(self.cache_dir, '2020', '*')) ]
        dataset_names = [ os.path.basename(p) for p in glob(os.path.join(backup_dir, '*'))]
        self.assert_(set(dataset_names).issubset(set(expected_dataset_names)))
        self.assertEqual(set(dataset_names).symmetric_difference( set(expected_dataset_names) ), set([]) )

    def test_doing_refinements_from_specified_refinement_dataset(self):
        self.prepare_cache()
        os.system("%(python)s %(script)s -c %(cache_directory)s -s %(start_year)s -e %(end_year)s --refinements-directory=%(refinement_directory)s" % 
                  {'python': sys.executable, 'script': self.script, 'cache_directory': self.cache_dir,
                   'start_year': 2021, 'end_year': 2022,
                   'refinement_directory': os.path.join(self.cache_dir, '2000')}
                  )
        
        simulation_state = SimulationState()
        
        ## test refinement for 2021
        simulation_state.set_current_time(2021)
        jobs = self.dataset_pool.get_dataset('job')
        buildings = self.dataset_pool.get_dataset('building')
        jobs13_raz3 = jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(parcel.raz_id==3, intermediates=[building]))', 
                                                  dataset_pool=self.dataset_pool)
        jobs13_raz4 = jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(parcel.raz_id, intermediates=[building])==4)', 
                                                  dataset_pool=self.dataset_pool)
        jobs13_raz5 = jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(parcel.raz_id, intermediates=[building])==5 )', 
                                                  dataset_pool=self.dataset_pool)
        jobs_raz5 = jobs.compute_variables('job.disaggregate(parcel.raz_id, intermediates=[building])==5', 
                                                dataset_pool=self.dataset_pool)
        
        #check results
        self.assertEqual(jobs13_raz3.sum(), 0)
        self.assertEqual(jobs13_raz4.sum(), 0)
        self.assertEqual(jobs13_raz5.sum() >= 5, True)
        self.assertEqual(jobs_raz5.sum(), 7)
        expected_nr_sqft = array([6, 0, 3, 6, 1, 6, 5, 0])
        ## was             array([6, 2, 3, 6, 1, 2, 5, 0]),
        self.assert_(allclose(buildings.get_attribute('non_residential_sqft'),  expected_nr_sqft))
        
        self.dataset_pool.remove_all_datasets()
        
        
        ## test refinement for 2022
        simulation_state.set_current_time(2022)
        hhs = self.dataset_pool.get_dataset('household')
        buildings = self.dataset_pool.get_dataset('building')
        
        hhs_raz6 = hhs.compute_variables('household.disaggregate(building.disaggregate(parcel.raz_id)==6)', 
                                              dataset_pool=self.dataset_pool)
        hhs_bldg = buildings.compute_variables('building.number_of_agents(household)', 
                                                    dataset_pool=self.dataset_pool)
        
        #check results
        self.assertEqual(hhs_raz6.sum(), 7)
        self.assert_(hhs_bldg.sum(),  7 )
        self.assert_((hhs_bldg!=0).sum(),  2)
        self.assert_(buildings.get_attribute('residential_units').sum(),  7)
        
        self.dataset_pool.remove_all_datasets()        
        
        
    def test_doing_other_refinements(self):
        self.prepare_cache()
        os.system("%(python)s  %(script)s -c %(cache_directory)s -s %(start_year)s -e %(end_year)s" % 
                  {'python': sys.executable, 'script': self.script, 'cache_directory':self.cache_dir,
                   'start_year': 2023, 'end_year': 2027 }
                  )        
        
        
        simulation_state = SimulationState()
                
        ## test refinement for 2023
        simulation_state.set_current_time(2023)
        hhs = self.dataset_pool.get_dataset('household')
        
        hhs_p5 = hhs.compute_variables('household.persons>5')
        
        #check results
        self.assert_(hhs.size(),  2)
        self.assertEqual(hhs_p5.sum(), 0)
        
        self.dataset_pool.remove_all_datasets()
        
        ## test refinement for 2027
        simulation_state.set_current_time(2027)
        hhs = self.dataset_pool.get_dataset('household')
        buildings = self.dataset_pool.get_dataset('building')
        persons = self.dataset_pool.get_dataset('person')
        
        
        hhs_raz6 = hhs.compute_variables('household.disaggregate(building.disaggregate(parcel.raz_id)==6)', 
                                              dataset_pool=self.dataset_pool)
        hhs_bldg = buildings.compute_variables('building.number_of_agents(household)', 
                                                    dataset_pool=self.dataset_pool)
        
        #check results
        self.assertEqual(hhs_raz6.sum(), 3)
        self.assert_(hhs_bldg.sum(),  3 )
        self.assert_((hhs_bldg!=0).sum(),  2)
        self.assert_(allclose(persons.get_attribute('job_id'), array([-1,  -1, -1, -1,  3,  4,  7])))

        
if __name__=='__main__':
    opus_unittest.main()
    