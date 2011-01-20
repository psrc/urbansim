# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array

from opus_core.configuration import Configuration


class AddProjectsToBuildingsConfigurationCreator(object):
    _model_name = 'add_projects_to_buildings'
    
    def __init__(self,
        input_projects = 'dptm_results',
        building_set = 'building',
        building_type_set = 'building_type', 
        location_id_name = 'zone_id', 
        units_names = {} # use single quotes for any string inside of the dictionary
        ):
        
        self.input_projects = input_projects
        self. building_set = building_set
        self. building_type_set = building_type_set
        self.location_id_name = location_id_name
        self.units_names = units_names
    
    def execute(self):
        return Configuration({
            'import': {
                'urbansim_zone.models.%s' % self._model_name: 'AddProjectsToBuildings'
                },
            'init': {'name': 'AddProjectsToBuildings'},
            'run': {
                'arguments': {
                    'projects': self.input_projects,
                    'building_set': self.building_set,
                    'building_type_set': self.building_type_set,
                    'location_id_name': "'%s'" % self.location_id_name,
                    'units_names': "%s" % self.units_names
                    },
                }
            })
            

from opus_core.tests import opus_unittest 


class TestAddProjectsToBuildingsConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = AddProjectsToBuildingsConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim_zone.models.add_projects_to_buildings': 'AddProjectsToBuildings'
                },
            'init': {'name': 'AddProjectsToBuildings'},
            'run': {
                'arguments': {
                    'projects': 'dptm_results',
                    'building_set': 'building',
                    'building_type_set': 'building_type',
                    'location_id_name': "'zone_id'",
                    'units_names': "{}"
                    },
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = AddProjectsToBuildingsConfigurationCreator(
            input_projects = 'input_projects',
            units_names = {'residential': 'my_units', 'commercial': 'job_spaces'}
            )
        
        expected = Configuration({
            'import': {
                'urbansim_zone.models.add_projects_to_buildings': 'AddProjectsToBuildings'
                },
            'init': {'name': 'AddProjectsToBuildings'},
            'run': {
                'arguments': {
                    'projects': 'input_projects',
                    'building_set': 'building',
                    'building_type_set': 'building_type',
                    'location_id_name': "'zone_id'",
                    'units_names': "{'residential': 'my_units', 'commercial': 'job_spaces'}"
                    },
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()
