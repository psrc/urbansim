# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import pickle, time, sys, string, io
#from bayarea.pyaccess import PyAccess
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy
from numpy import ones, array

class AddDpa(Model):
    """Executes experimental code.
    """
    model_name = "Add DPA"

    def run(self):
        """Runs the add dpa model. 
        """
        dataset_pool = SessionConfiguration().get_dataset_pool()

        job_set = dataset_pool.get_dataset('job')

        household_set = dataset_pool.get_dataset('household')

        submarket_set = dataset_pool.get_dataset('submarket')

        employment_submarket_set = dataset_pool.get_dataset('employment_submarket')

        building_set = dataset_pool.get_dataset('building')
        
        zone_set = dataset_pool.get_dataset('zone')

        employment_submarket_set.add_attribute(name='dpa_id', data=employment_submarket_set.compute_variables('employment_submarket.disaggregate(zone.dpa_id)'))

        submarket_set.add_attribute(name='dpa_id', data=submarket_set.compute_variables('submarket.disaggregate(zone.dpa_id)'))

        job_dpa = job_set.compute_variables('job.disaggregate(employment_submarket.dpa_id)')

        household_dpa = household_set.compute_variables('household.disaggregate(submarket.dpa_id)')
        
        household_zone = household_set.compute_variables('household.disaggregate(parcel.zone_id,intermediates=[building])')

        job_set.add_primary_attribute(name='dpa_id', data=job_dpa)

        household_set.add_primary_attribute(name='dpa_id', data=household_dpa)
        
        household_set.add_primary_attribute(name='household_zone', data=household_zone)