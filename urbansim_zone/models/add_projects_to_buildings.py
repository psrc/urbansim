#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.model import Model
from opus_core.logger import logger

class AddProjectsToBuildings(Model):

    model_name = "add_projects_to_buildings"

    def run(self, projects, building_set, building_type_set, location_id_name="zone_id", units_names = {}):
        """Modify buildings to reflect these development projects. Will work only with the PseudoBuildingDataset (and its children).
           units_names is a dictionary that holds for each project type the name of the building attribute to update.
           By default the same attribute name as in the project dataset is taken. 
        """
        project_types = projects.keys()
        project_units_names = units_names
        for ptype in project_types:
            if projects[ptype] is None:
                continue
            if (ptype not in project_units_names.keys()):
                 # attributes that are not id names 
                project_units_names[ptype] = [x for x in projects[ptype].get_primary_attribute_names() if x not in projects[ptype].get_id_name()][0]
            type_id = building_type_set.get_code(ptype)
            bldgs_ids = building_set.get_ids_of_locations_and_type(locations= projects[ptype].get_attribute(location_id_name), type_id=type_id)
            idx = building_set.get_id_index(bldgs_ids)
            current_values = building_set.get_attribute_by_index(project_units_names[ptype], idx)
            building_set.modify_attribute(name=project_units_names[ptype], data = current_values + projects[ptype].get_attribute(projects[ptype].get_attribute_name()), 
                                          index=idx)

from numpy import arange, array, ma
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset

class AddProjectsToBuildingsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = StorageFactory().get_storage('dict_storage')
        self.storage.write_table(
            table_name='pseudo_buildings',
            table_data={
                "pseudo_building_id": arange(1,31), # 1 building per building_type and zone
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
        self.buildings = self.dataset_pool.get_dataset('pseudo_building')
        self.building_types = self.dataset_pool.get_dataset('building_type')

    def test_add_nothing(self):
        projects = {'residential': None, 'commercial': None, 'industrial': None}
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings, self.building_types)
        self.assert_(ma.equal(self.buildings.get_attribute("residential_units"), array(10*[200, 0, 0])).all())
        self.assert_(ma.equal(self.buildings.get_attribute("commercial_job_spaces"), array(10*[0, 100, 0])).all())
        self.assert_(ma.equal(self.buildings.get_attribute("industrial_job_spaces"), array(10*[0, 0, 100])).all())

    def test_add_one_project(self):
        projects = {'residential': None, 
                    'commercial': self.get_projects('commercial', {'project_id': arange(1,5),
                                                                   'commercial_job_spaces': array(3*[20]+[5]), 
                                                                   'zone_id': arange(1,5)}, 
                                                    'commercial_job_spaces'),
                    'industrial': None}
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings, self.building_types)
        self.assert_(ma.equal(self.buildings.get_attribute("residential_units"), array(10*[200, 0, 0])).all())
        self.assert_(ma.equal(self.buildings.get_attribute("commercial_job_spaces"), array(3*[0, 120, 0] + [0,105,0] + 6*[0, 100, 0])).all())
        self.assert_(ma.equal(self.buildings.get_attribute("industrial_job_spaces"), array(10*[0, 0, 100])).all())

    def test_add_three_projects(self):
        projects = {'residential': self.get_projects('residential', {'project_id': arange(1,6),
                                                                     'residential_units': array([100, 300, 1, 50, 6]),
                                                                     'zone_id': array([3, 5, 7, 8, 10])},
                                                    'residential_units'),

                    'commercial': self.get_projects('commercial', {'project_id': arange(1,5),
                                                                   'commercial_job_spaces': array(3*[20]+[5]),
                                                                   'zone_id': arange(1,5)},
                                                    'commercial_job_spaces'),
                    'industrial': self.get_projects('industrial', {'project_id': arange(1,3),
                                                                   'industrial_job_spaces': array([50, 30]),
                                                                   'zone_id': array([2,10])},
                                                    'industrial_job_spaces'),
}
        m = AddProjectsToBuildings()
        m.run(projects, self.buildings, self.building_types)
        self.assert_(ma.equal(self.buildings.get_attribute("residential_units"), 
                                        array([200, 0, 0, 200, 0, 0, 200, 0, 0, 200, 0, 0, 200, 0, 0, 200, 0, 0, 200, 0, 0, 200,0, 0, 200, 0, 0, 200, 0, 0])).all())
        self.assert_(ma.equal(self.buildings.get_attribute("commercial_job_spaces"), array(3*[0, 120, 0] + [0,105,0] + 6*[0, 100, 0])).all())
        self.assert_(ma.equal(self.buildings.get_attribute("industrial_job_spaces"), 
                                        array([0,0,100, 0,0,150] + 7*[0, 0, 100] + [0,0,130])).all())

    def get_projects(self, project_type, data, units_attribute):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='development_projects',
                            table_data=data)
        return DevelopmentProjectDataset(
            in_storage = storage,
            in_table_name = 'development_projects',
            what = project_type,
            attribute_name = units_attribute,
            )


if __name__=="__main__":
    opus_unittest.main()

