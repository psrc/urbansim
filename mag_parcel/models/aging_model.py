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

class AgingModel(Model):
    """ This model adds the number specified by the 'number_of_years' argument
        to the dataset and attribute specified in any number of entries into the
        dictionary specified by datasets.
        
        datasets should be a dictionary of the form {'dataset_name':'attribute_name'},
        and can contain any number of entries for aging
        
        number_of_years should be an integer > 0
        
        For instance, passing in these arguments to the run() method:
        datasets = {'person':'age','household':'age_of_head'}
        number_of_years = 1
        will advance the 'age' attribute of the 'person' dataset and the 'age_of_head'
        attribute of the 'household' attribute each by one.
    """
    model_name = "Aging Model"

    def run(self, datasets, number_of_years, dataset_pool=None):
        # Check for strange values for aging
        number_of_years = int(number_of_years)
        if number_of_years < 1:
            logger.log_warning("You are aging with a number less than 1")
        
        for i in datasets.items():
            # Grab the dataset and attribute to age
            dataset_to_age = dataset_pool.get_dataset(i[0])
            attribute_to_age = dataset_to_age.get_attribute(i[1])
            # Add the number_of_years to the attribute to age
            aged_attribute = attribute_to_age+int(number_of_years)
            logger.log_status("Aging '%s' attribute of '%s' dataset by '%s' year(s)" % (i[1],i[0],str(number_of_years)))
            # Modify the dataset with the aged values
            dataset_to_age.modify_attribute(i[1], aged_attribute)
        return
    
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import arange, array

class AgingModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        household_data = {
            'household_id': arange(10)+1,
            'age_of_head': array([20, 23, 22, 21, 31, 41, 43, 52, 62, 73])
                         }
        person_data = {
            'person_id': arange(10)+1,
            'age': array([21, 25, 29, 23, 37, 42, 40, 54, 61, 77])
                      }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'households', table_data = household_data)
        storage.write_table(table_name = 'persons', table_data = person_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['opus_core'])
        self.households = self.dataset_pool.get_dataset('household')
        self.persons = self.dataset_pool.get_dataset('person')
        
    def test_aging_model(self):
        # Initialize model
        model = AgingModel()
        
        # Set up arguments
        datasets_dict = {'household':'age_of_head','person':'age'}
        num_years = 1
        
        # Run model
        model.run(datasets_dict, num_years, self.dataset_pool)
        
        # Check model answers
        self.assertEqual(self.persons.get_attribute('age')[0], 22)
        self.assertEqual(self.persons.get_attribute('age')[1], 26)
        self.assertEqual(self.persons.get_attribute('age')[2], 30)
        self.assertEqual(self.persons.get_attribute('age')[3], 24)
        self.assertEqual(self.persons.get_attribute('age')[4], 38)
        self.assertEqual(self.persons.get_attribute('age')[5], 43)
        self.assertEqual(self.persons.get_attribute('age')[6], 41)
        self.assertEqual(self.persons.get_attribute('age')[7], 55)
        self.assertEqual(self.persons.get_attribute('age')[8], 62)
        self.assertEqual(self.persons.get_attribute('age')[9], 78)
        self.assertEqual(self.households.get_attribute('age_of_head')[0], 21)
        self.assertEqual(self.households.get_attribute('age_of_head')[1], 24)
        self.assertEqual(self.households.get_attribute('age_of_head')[2], 23)
        self.assertEqual(self.households.get_attribute('age_of_head')[3], 22)
        self.assertEqual(self.households.get_attribute('age_of_head')[4], 32)
        self.assertEqual(self.households.get_attribute('age_of_head')[5], 42)
        self.assertEqual(self.households.get_attribute('age_of_head')[6], 44)
        self.assertEqual(self.households.get_attribute('age_of_head')[7], 53)
        self.assertEqual(self.households.get_attribute('age_of_head')[8], 63)
        self.assertEqual(self.households.get_attribute('age_of_head')[9], 74)
