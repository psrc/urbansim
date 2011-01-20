# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

#DISCLAIMER: THIS FILE IS OUT OF DATE AND NEEDS SIGNIFICANT MODIFICATIONS 
#            TO MAKE IT WORK

import os
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.development_types import DevelopmentTypeDataset
from urbansim.datasets.employment_sector_groups import EmploymentSectorGroupDataset
from urbansim.datasets.travel_data import TravelDataDataset
from urbansim.datasets.rate_dataset import RateDataset
from urbansim.datasets.race_dataset import RaceDataset
from urbansim.datasets.neighborhood_dataset import NeighborhoodDataset
from urbansim.datasets.faz_dataset import FazDataset
from paris_sandbox.employment_location_choice_model_creator import EmploymentLocationChoiceModelCreator
#from urbansim.models.employment_industrial_location_choice_model_creator import EmploymentIndustrialLocationChoiceModelCreator
#from urbansim.datasets.target_vacancies import TargetVacancyDataset
#from urbansim.datasets.development_projects import create_residential_projects_from_history
#from urbansim.models.development_project_transition_model import DevelopmentProjectTransitionModel
#from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
from sandbox.example_gridcells import DB_settings
from opus_core.coefficients import Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory
from opus_core.store.opus_database import OpusDatabase
from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from numpy import arange, where
from time import time
from paris.paris_settings import ParisSettings
from opus_core.storage_factory import StorageFactory
 

def create_jobs_for_estimation(agent_set, dbcon):
        
        estimation_set.load_dataset(attributes='*')
        agent_set.load_dataset(attributes='*')
        job_ids = estimation_set.get_id_attribute()
        index = agent_set.get_id_index(job_ids)
        for attr in estimation_set.get_attribute_names():
            agent_set.set_values_of_one_attribute(attr, estimation_set.get_attribute(attr), index)
        return (agent_set, index)

class This_Settings(ParisSettings):
    settings = ParisSettings()
    
class Paris_simulation(object):
    def run(self, nbs, jobs, data_objects, dbcon, variables=(), coefficients=(), submodels=(), \
            debuglevel=0):
        t1 = time()
        l=len(variables)
        print variables,coefficients,submodels
        specification = EquationSpecification(variables=variables, coefficients=coefficients, submodels=submodels)
        
#        storage = StorageFactory().get_storage(type='mysql_storage', storage_location=dbcon)
        
#        specification = EquationSpecification(storage=storage)
#        specification.load(place="employment_non_home_based_location_choice_model_specification")
#        coefficients = Coefficients(storage=storage)
#        coefficients.load(place="employment_commercial_location_choice_model_coefficients")

        elcm = EmploymentLocationChoiceModelCreator().get_model(location_set=nbs,
            sample_size_locations = 10)  # choice set size (includes current location)
      
        ##save estimation results
        con = OpusDatabase(hostname=DB_settings.db_host_name,
                           username=DB_settings.db_user_name, 
                           password=DB_settings.db_password,
                           database_name=This_Settings.outputdb)
            
        estimation_set = JobDataset(in_storage=StorageFactory().get_storage('sql_storage', storage_location=dbcon),
            in_place="jobs_for_estimation")

        result = elcm.estimate(specification, agent_set=estimation_set, data_objects=data_objects,
                debuglevel=debuglevel)

        #save estimation results
#        save_object(specification, 'employment_location_choice_model_specification', type='mysql_storage', base=con)
#        save_object(result[0], 'employment_location_choice_model_coefficients', type='mysql_storage', base=con)

        print "Simulation done. " + str(time()-t1) + " s"

class Run_Paris_Simulation(object):
    def __init__(self, variables=(), coefficients=(), submodels=(), debuglevel=0):
        # neighborhoods, jobs and households are loaded from disk ('flt_storage'), other objects from mysql. Change it as you need.
        self.nbs = NeighborhoodDataset(in_storage=StorageFactory().get_storage('flt_storage', storage_location=This_Settings.dir),
                in_place=This_Settings.nbsubdir, \
                out_storage=StorageFactory().get_storage('flt_storage', storage_location = This_Settings.outputdir), 
                debuglevel=debuglevel)
        self.jobs = JobDataset(in_base = This_Settings.dir, in_storage=StorageFactory().get_storage('flt_storage', storage_location=This_Settings.dir),
            out_storage=StorageFactory().get_storage('flt_storage', storage_location = This_Settings.outputdir),
                in_place=This_Settings.jobsubdir, debuglevel=debuglevel)
        Con = OpusDatabase(hostname=DB_settings.db_host_name,
                           username=DB_settings.db_user_name, 
                           password=DB_settings.db_password, 
                           database_name=This_Settings.db)
        self.hhs = HouseholdDataset(in_base = This_Settings.dir, in_storage=StorageFactory().get_storage('flt_storage', storage_location=This_Settings.dir), 
            out_storage=StorageFactory().get_storage('flt_storage', storage_location=This_Settings.outputdir),
                in_place=This_Settings.hhsubdir, debuglevel=debuglevel)
        self.resources=Resources({"household":self.hhs,"job":self.jobs})
        #simulate
        Paris_simulation().run(nbs=self.nbs, jobs=self.jobs, \
                data_objects=self.resources,\
                dbcon=Con, variables=variables, coefficients=coefficients, submodels=submodels, debuglevel=debuglevel)
        Con.close_connection()

class Generic_specification(object):
    def __init__(self):
        self.submodels = []
        self.variables = []
        self.coefficients = []
        for i in range(15):
            variable = ("is_paris","ln_residential_units","ln_price", \
            "tc","vp","young","poor_m")
            self.variables += variable
            submodel = i+1
            self.submodels += [submodel]*len(variable)
        self.coefficients = self.variables # or put your own names for coefficients here (as a tuple)
                                 # in the same order as 'variables'                             
if __name__ == "__main__":
    # run estimation for the given variables
    spec = Generic_specification()
    sim = Run_Paris_Simulation(variables=spec.variables, coefficients=spec.coefficients, submodels=spec.submodels, debuglevel=4) 

