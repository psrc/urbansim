# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.session_configuration import SessionConfiguration
from opus_core.model import Model
import os
#from opus_core.datasets.dataset import Dataset, DatasetSubset
#from opus_core.logger import logger
from numpy import ones, zeros, array
# Add: Import some numpy functions for prob sample --Hanyi
#from numpy import searchsorted, cumsum, float64, array
#from numpy.random import uniform
#import sys
# End

class TestModel(Model):

    model_name = "Test Model"

    def run(self):
        #os.popen('python C:\\opus\\src\\trunk\\mag_zone\\tools\\create_zone_simulation_report_excel.py')
        #print 'Hello World'
        # Get the dataset pool
        dataset_pool = SessionConfiguration().get_dataset_pool()
        buildings_dataset = dataset_pool.get_dataset('building')
        building_type_id = buildings_dataset.get_attribute('building_type_id')
        indx = array(range(1,11))
        print '\n'
        print 'indx = %s' % indx
        new_data = zeros(shape=10,dtype=building_type_id.dtype)
        print '\n'
        print 'new_data = %s' % new_data
        
        indicies_of_indx_on_buildings = buildings_dataset.get_id_index(indx)
        print '\n'
        print 'indicies_of_indx_on_buildings = %s' % indicies_of_indx_on_buildings
        buildings_dataset.set_values_of_one_attribute('building_type_id',new_data,indicies_of_indx_on_buildings)