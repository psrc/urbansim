# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.misc import digits
from numpy import column_stack, row_stack, where, unique
from scipy import ndimage

class AddProjectsToBuildings(Model):

    model_name = "Add Development Projects Quantity to Buildings"

    def run(self, developmentproject_dataset, building_dataset, 
            label_attribute_names=["building_type_id", "zone_id"], 
            quantity_attribute_names = ["residential_units", "non_residential_sqft"]):
        """Modify buildings to reflect new development projects. 
        """
        
        project_labels = None
        building_labels = None
        
        if not developmentproject_dataset or developmentproject_dataset.size() == 0:
            logger.log_warning("Empty development project dataset; Will do nothing.")
            return building_dataset

        for label_attribute in label_attribute_names:
            project_label_attribute = developmentproject_dataset.get_attribute_as_column(label_attribute)
            building_lable_attribute = building_dataset.get_attribute_as_column(label_attribute)
            if project_labels is None:
                project_labels = project_label_attribute
            else:
                project_labels = column_stack((project_labels, project_label_attribute))
                
            if building_labels is None:
                building_labels = building_lable_attribute
            else:
                building_labels = column_stack((building_labels, building_lable_attribute))
        max_digits = digits( row_stack((project_labels, building_labels)).max(axis=0) )
        multipler = array([10**d for d in max_digits[1:] + [0]])
        project_identifier = (project_labels * multipler).sum(axis=1)
        unique_project_identifier = unique(project_identifier)
        building_identifier = (building_labels * multipler).sum(axis=1)
        
        for quantity_attribute in quantity_attribute_names:
            quantity_sum = ndimage.sum(developmentproject_dataset.get_attribute(quantity_attribute), labels=project_identifier, index=unique_project_identifier)
            for i in range(unique_project_identifier.size):
                this_identifier = unique_project_identifier[i]
                this_label = []
                remain = this_identifier
                for m in multipler:
                    this_label.append(remain // m)
                    remain = remain % m
                building_index = where(building_identifier==this_identifier)[0]
                #assert building_index.size == 1
                if building_index.size == 0:
                    logger.log_error("building with attribute (%s) = (%s) is not in building_dataset" % (label_attribute_names, this_label) )
                    continue
                    #for attribute in []:
                        #data = None
                    #building_dataset.add_elements(name=quantity_attribute, data = current_values+quantity_sum[i], 
                                                  #index=building_index)
                if building_index.size > 1:
                    logger.log_warning("There are more than 1 building with attributes (%s) = (%s)" % (label_attribute_names, this_label) )
                    building_index = building_index[0]
                current_values = building_dataset.get_attribute_by_index(quantity_attribute, building_index)
                building_dataset.modify_attribute(name=quantity_attribute, data = current_values+quantity_sum[i], 
                                                  index=building_index)
        return building_dataset
                
from numpy import arange, array, ma
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset

class AddProjectsToBuildingsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = StorageFactory().get_storage('dict_storage')
        self.storage.write_table(
            table_name='buildings',
            table_data={
                "building_id": arange(1,31), # 1 building per building_type and zone
                "zone_id": array( [1,1,1, 2,2,2, 3,3,3, 4,4,4, 5,5,5, 6,6,6, 7,7,7, 8,8,8, 9,9,9, 10,10,10] ),
                "building_type_id": array(10*[1,2,3]),
                "residential_units": array(10*[200, 0, 0]),
                "commercial_job_spaces": array(10*[0,100,0]),
                "industrial_job_spaces": array(10*[0,0,100]),
                }
            )
        self.storage.write_table(
            table_name='building_types',
            table_data={
                "building_type_id":array([1,2,3]),
                "name": array(["residential", "commercial", "industrial"]),
                }
            )
        self.dataset_pool = DatasetPool(package_order=['urbansim_zone', "urbansim"],
                                        storage=self.storage)
        self.buildings = self.dataset_pool.get_dataset('building')
        self.building_types = self.dataset_pool.get_dataset('building_type')

    def test_add_nothing(self):
        projects = None
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("residential_units"), array(10*[200, 0, 0])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("commercial_job_spaces"), array(10*[0, 100, 0])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("industrial_job_spaces"), array(10*[0, 0, 100])), True)

    def test_add_one_project(self):
        project_data = {'project_id': arange(1,5),
                        'commercial_job_spaces': array(3*[20]+[5]), 
                        'zone_id': arange(1,5), 
                        'building_type_id': array([2]*4)
                        }
        projects = self.get_projects(project_data)
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings, quantity_attribute_names = ["commercial_job_spaces"])
        self.assertEqual(ma.allequal(self.buildings.get_attribute("residential_units"), array(10*[200, 0, 0])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("commercial_job_spaces"), array(3*[0, 120, 0] + [0,105,0] + 6*[0, 100, 0])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("industrial_job_spaces"), array(10*[0, 0, 100])), True)

    def test_add_three_projects(self):
        project_data = {'project_id': arange(1,12), 
                        'zone_id': array([3, 5, 7, 8, 10] + range(1,5) + [2,10]), 
                        'building_type_id': array([1]*5 + [2]*4 + [3]*2),
                        'residential_units': array([100, 300, 1, 50, 6]+4*[0]+2*[0]),
                        'commercial_job_spaces': array(5*[0]+3*[20]+[5]+2*[0]),
                        'industrial_job_spaces': array(5*[0]+4*[0]+[50, 30]),
                        }
        
        projects = self.get_projects(project_data)
        
#        projects = {'residential': self.get_projects('residential', {'project_id': arange(1,6),
#                                                                     'residential_units': array([100, 300, 1, 50, 6]),
#                                                                     'zone_id': array([3, 5, 7, 8, 10])},
#                                                    'residential_units'),
#
#                    'commercial': self.get_projects('commercial', {'project_id': arange(1,5),
#                                                                   'commercial_job_spaces': array(3*[20]+[5]),
#                                                                   'zone_id': arange(1,5)},
#                                                    'commercial_job_spaces'),
#                    'industrial': self.get_projects('industrial', {'project_id': arange(1,3),
#                                                                   'industrial_job_spaces': array([50, 30]),
#                                                                   'zone_id': array([2,10])},
#                                                    'industrial_job_spaces'),
#}
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings, quantity_attribute_names = ["residential_units", "commercial_job_spaces", "industrial_job_spaces"])
        self.assertEqual(ma.allequal(self.buildings.get_attribute("residential_units"), 
                                        array([200,0,0, 200,0,0, 300,0,0, 200,0,0, 500,0,0, 200,0,0, 201,0,0, 250,0,0, 200,0,0, 206,0,0,])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("commercial_job_spaces"), array(3*[0, 120, 0] + [0,105,0] + 6*[0, 100, 0])), True)
        self.assertEqual(ma.allequal(self.buildings.get_attribute("industrial_job_spaces"), 
                                        array([0,0,100, 0,0,150] + 7*[0, 0, 100] + [0,0,130])), True)

    def get_projects(self, data):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='development_projects',
                            table_data=data)
        return Dataset(
            id_name = "project_id",
            in_storage = storage,
            in_table_name = 'development_projects',
            dataset_name = "development_project",
            )

if __name__=="__main__":
    opus_unittest.main()

