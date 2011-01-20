# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from numpy import where

class AddProjectsToBuildings(Model):

    model_name = "add_projects_to_buildings"

    def run(self, project_set, building_set):
        """Modify buildings to reflect these development projects.
        """
        if project_set is None:
            logger.log_status('Nothing to be done.')
            return
        bldgs_ids = project_set.get_attribute('building_id')
        placed_idx = where(bldgs_ids>0)[0]
        idx_in_buildings = building_set.get_id_index(bldgs_ids[placed_idx])
        for units in ["residential_units", "non_residential_sqft"]:
            current_values = building_set.get_attribute_by_index(units, idx_in_buildings)
            building_set.modify_attribute(name=units, data = current_values + project_set.get_attribute(units)[placed_idx], 
                                          index=idx_in_buildings)
            
from numpy import arange, array, ma
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset
from opus_core.datasets.dataset import Dataset

class AddProjectsToBuildingsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = StorageFactory().get_storage('dict_storage')
        self.storage.write_table(
            table_name='buildings',
            table_data={
                "building_id": arange(1,31),
                "residential_units": array(10*[200, 0, 0]),
                "non_residential_sqft": array(10*[0,100,50]),
                }
            )
        self.dataset_pool = DatasetPool(package_order=['urbansim_zone', "urbansim"],
                                        storage=self.storage)
        self.buildings = self.dataset_pool.get_dataset('building')

    def test_add_nothing(self):
        projects = None
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("residential_units"), array(10*[200, 0, 0])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("non_residential_sqft"), array(10*[0, 100, 50])), True)

    def test_add_projects(self):
        storage = StorageFactory().get_storage('dict_storage')
        data = {"project_id": arange( 1,7 ),
                "residential_units": array( 4*[0]+[10, 34]),
                "non_residential_sqft": array(3*[20]+[5]+[0,0]),
                'building_type_id': array(4*[1]+2*[4]),
                "building_id": array([5, 10, 12, 20, 27, 25])}

        storage.write_table(table_name='development_projects', table_data=data)

        projects = Dataset(
            in_storage = storage,
            in_table_name = 'development_projects',
            id_name='project_id'
            )
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("residential_units"), 
                                     array(8*[200, 0, 0]+[234, 0, 10, 200, 0, 0])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("non_residential_sqft"), array(
                                    [0, 100, 50, 0, 120, 50, 0, 100, 50, 20, 100, 70, 0, 100, 50, 0, 100, 50, 0, 105, 50] + 3*[0, 100, 50]
                                                                                )), True)



if __name__=="__main__":
    opus_unittest.main()

