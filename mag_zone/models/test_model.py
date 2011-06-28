# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.model import Model
import os
#from opus_core.datasets.dataset import Dataset, DatasetSubset
#from opus_core.logger import logger
#from numpy import where, ones, zeros, logical_and, clip, round_
# Add: Import some numpy functions for prob sample --Hanyi
#from numpy import searchsorted, cumsum, float64, array
#from numpy.random import uniform
#import sys
# End

class TestModel(Model):

    model_name = "Test Model"

    def run(self):
        #os.popen('python C:\\opus\\src\\trunk\\mag_zone\\tools\\create_zone_simulation_report_excel.py')
        print 'Hello World'
