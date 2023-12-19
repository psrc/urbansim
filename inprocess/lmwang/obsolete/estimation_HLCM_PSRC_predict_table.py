# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus.urbansim.datasets.gridcells import GridcellSet
from opus.urbansim.datasets.jobs import JobSet
from opus.urbansim.datasets.households import HouseholdSet
from opus.urbansim.datasets.development_types import DevelopmentTypeSet
from opus.urbansim.datasets.development_groups import DevelopmentGroupSet
from opus.urbansim.datasets.employment_sectors import EmploymentSectorSet
from opus.urbansim.datasets.employment_sector_groups import EmploymentSectorGroupSet
from opus.urbansim.datasets.rates import RateSet
from opus.urbansim.datasets.races import RaceSet
from opus.urbansim.datasets.zones import ZoneSet
from opus.urbansim.datasets.fazes import FazSet
from opus.urbansim.datasets.fazdistricts import FazdistrictSet
from opus.urbansim.datasets.target_vacancies import TargetVacancySet
from opus.urbansim.datasets.development_projects import create_residential_projects_from_history
from opus.urbansim.models.development_project_transition_model import DevelopmentProjectTransitionModel
from opus.urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
from opus.sandbox.example_gridcells import DB_settings
from opus.urbansim.constants import read_constants_from_DB
from opus.core.coefficients import Coefficients
from opus.core.equation_specification import EquationSpecification
from opus.urbansim.storage_creator import StorageCreator
from opus.urbansim.store.scenario_database import DbConnection
from opus.core.dataset import DataSet, AttributeMetaData, DataSubset
from opus.core.resources import Resources
from opus.core.sampling_functions import sample_choice
from numarray.random_array import seed, permutation
from opus.core.opusnumarray import sum
from numarray import arange, where, concatenate, zeros, Float32
from numarray.ma import filled
from time import time
import copy

 
def get_data_objects_from_DB(con, debuglevel=0):
    # probably not all these objects are needed 
    constants = read_constants_from_DB(con)
    devtypes = DevelopmentTypeSet(in_base = con, in_storage_type="MySQL", debuglevel=debuglevel)
    devgroups = DevelopmentGroupSet(in_base = con, in_storage_type="MySQL", debuglevel=debuglevel)
    empsectors = EmploymentSectorSet(in_base = con, in_storage_type="MySQL", debuglevel=debuglevel)
    empgroups = EmploymentSectorGroupSet(in_base = con, in_storage_type="MySQL", debuglevel=debuglevel)
    zones = ZoneSet(in_base = con, in_storage_type="MySQL", \
        other_in_places=[], debuglevel=debuglevel)
    races = RaceSet(in_base = con, in_storage_type="MySQL", debuglevel=debuglevel)
    try:
        #fazes = FazSet(zoneset=zones)
        fazes = FazSet(in_base=con, in_storage_type="MySQL", in_place="fazes")
    except:
        fazes=None
        
    try:
        fazdistricts = FazdistrictSet(fazset=fazes)
    except:
        fazdistricts=None        
    resources = {"constants":constants, "development_type":devtypes, "zone":zones, "faz":fazes, \
        "development_group":devgroups, "employment_sector":empsectors, "employment_sector_group":empgroups, \
        "fazdistrict":fazdistricts, "race":races}
    return resources


def create_households_for_estimation(agent_set, dbcon):
        estimation_set = HouseholdSet(in_base = dbcon, in_storage_type="mysql", \
                in_place="households_for_estimation")
        agent_set.unload_nonderived_attributes()
        agent_set.load_dataset(attributes='*')
        estimation_set.load_dataset(agent_set.get_nonderived_attribute_names())
        for attr in agent_set.get_attribute_names():
            agent_set.set[attr].set_data(concatenate((estimation_set.set[attr].get_data(), agent_set.set[attr].get_data())))
        agent_set.update_id_mapping()
        agent_set.update_size()
        return (agent_set, arange(estimation_set.size()))
#        return (agent_set, arange(10))

def copy_dataset(dataset):
    attr_list = ['set', 'attribute_names', 'id_mapping', 'nonderived_attribute_names']
    new_dataset = copy.copy(dataset)
    for attr in attr_list:
        exec("new_dataset." + attr + " = copy.deepcopy(dataset." + attr + ")", globals())
    return new_dataset

def create_predict_table(LCM, agent_set, agents_index, observed_choices_id, data_objects, geographies=[]):

    resources = data_objects
    
    mc_choices = sample_choice(LCM.model.probabilities)    #monte carlo choice
    mc_choices_index = LCM.model_resources.translate("index")[mc_choices]
    maxprob_choices = sample_choice(LCM.model.probabilities, method="max_prob")  #max prob choice
    maxprob_choices_index = LCM.model_resources.translate("index")[maxprob_choices]
    results = []
    
    gcs = resources.translate("gridcell")
    for geography in geographies:
        geos = resources.translate(geography)
        
        #get observed geo_id
        obs = copy_dataset(agent_set)    
        obs.subset_by_index(agents_index)
        obs.set_values_of_one_attribute(gcs.id_name[0], observed_choices_id) 
    
        resources.merge({"household": obs}) #, "gridcell": gcs, "zone": zones, "faz":fazes})
        obs.compute_variables(geos.id_name[0], resources=resources)
        obs_geo_ids = obs.get_attribute(geos.id_name[0])
        
        #count simulated choices
        sim = copy_dataset(obs)
        sim.set_values_of_one_attribute(gcs.id_name[0], gcs.get_id_attribute()[mc_choices_index]) 
        resources.merge({"household": sim})
    
        geos_size = geos.size()
        geo_ids = geos.get_id_attribute()
        
        pred_matrix = zeros((geos_size, geos_size))
        p_success = zeros((geos_size,)).astype(Float32)
        
        f = 0
        for geo_id in geo_ids:
            index_in_geo = where(obs_geo_ids == geo_id)[0]
            resources.merge({"select_index": index_in_geo})
    
            geos.compute_variables("number_of_select_households", resources=resources)
            pred_matrix[f] = geos.get_attribute("number_of_select_households")
            if sum(pred_matrix[f]) > 0:
                p_success[f] = float(pred_matrix[f, f])/sum(pred_matrix[f])
    
            sim.increment_version('grid_id')  #to trigger recomputation in next iteration
            f += 1
            
        print(p_success)
        results.append((pred_matrix.copy(), p_success.copy()))
        
    return results
    

class PSRC_Settings:
    # change to your setting
#    dir = "f:/urbansim/data/GPSRC"
    dir = "/home/hana/urbansim/data/GPSRC"
#    dir = "../data/flt/GPSRC"
    outputdir = dir + "/output"
    gcsubdir = "gc"
    hhsubdir = "hh"
    jobsubdir = "jobs"
    zonesubdir = "zones"
    db = "PSRC_2000_baseyear_lmwang"

class PSRC_simulation:
    def run(self, gcs, jobs, hhs, data_objects, dbcon, variables=(), coefficients=(), \
            debuglevel=0):
        t1 = time()
        l=len(variables)
        specification = EquationSpecification(variables=variables, coefficients=coefficients) 
        hlcm = HouseholdLocationChoiceModelCreator().get_model(
            location_set = gcs,
            choices="urbansim.lottery_choices",
            sample_size_locations = 10)  # choice set size (includes current location)

        agent_set, observed_agents_index  =  create_households_for_estimation(hhs, dbcon)
        #half = observed_agents_index.size()
        agents_index_for_estimation = observed_agents_index#[:half]
        agents_index_for_simulation = observed_agents_index#[half:]

        est_results = hlcm.estimate(specification, agent_set=agent_set, \
                agents_index=agents_index_for_estimation, \
                data_objects=data_objects, debuglevel=debuglevel)
        coefficients = est_results[0]
        
        observed_choices_id = agent_set.get_attribute('grid_id')[agents_index_for_simulation]
        sim_results = hlcm.run(specification, coefficients=coefficients, agent_set=agent_set, \
                agents_index=agents_index_for_simulation, \
                data_objects=data_objects, debuglevel=debuglevel)
        
        create_predict_table(hlcm, hhs, agents_index_for_simulation, observed_choices_id, \
                             data_objects, geographies=['faz','fazdistrict'])
        print("Simulation done. " + str(time()-t1) + " s")

class Run_PSRCsimulation:
    def __init__(self, variables=(), coefficients=(), debuglevel=0):
        self.gcs = GridcellSet(in_base = PSRC_Settings.dir, in_storage_type="flt", \
                in_place=PSRC_Settings.gcsubdir, \
                out_storage_type="flt", out_base = PSRC_Settings.outputdir, debuglevel=debuglevel)
        self.jobs = JobSet(in_base = PSRC_Settings.dir, in_storage_type="flt", out_storage_type="flt", \
                in_place=PSRC_Settings.jobsubdir, out_base = PSRC_Settings.outputdir, debuglevel=debuglevel)
        self.hhs = HouseholdSet(in_base = PSRC_Settings.dir, in_storage_type="flt", out_storage_type="flt", \
                in_place=PSRC_Settings.hhsubdir, out_base = PSRC_Settings.outputdir, debuglevel=debuglevel)
        Con = DbConnection(db=PSRC_Settings.db, hostname=DB_settings.db_host_name, \
                username=DB_settings.db_user_name, password=DB_settings.db_password)
        #self.gcs = GridcellSet(in_base = Con, in_storage_type="mysql", \
                #out_storage_type="flt", out_base = PSRC_Settings.outputdir, debuglevel=debuglevel)
        #self.jobs = JobSet(in_base = Con, in_storage_type="mysql", out_storage_type="flt", \
                #out_base = PSRC_Settings.outputdir, debuglevel=debuglevel)
        #self.hhs = HouseholdSet(in_base = Con, in_storage_type="mysql", out_storage_type="flt", \
                #out_base = PSRC_Settings.outputdir, debuglevel=debuglevel)
        self.zones = ZoneSet(in_base = Con, in_storage_type="MySQL", out_storage_type="flt", \
                             out_base = PSRC_Settings.outputdir, debuglevel=debuglevel)
        
        self.data_objects = get_data_objects_from_DB(Con, debuglevel=debuglevel)
        self.resources = Resources(self.data_objects)
        self.resources.merge({"job":self.jobs, "gridcell":self.gcs, "household":self.hhs, "check_variables":[], "zone":self.zones})
#        vacanciestable = TargetVacancySet(in_base = Con)

        #simulate
        PSRC_simulation().run(gcs=self.gcs, jobs=self.jobs, hhs=self.hhs, \
                data_objects=self.resources,\
                dbcon=Con, variables=variables, coefficients=coefficients, debuglevel=debuglevel)
#        PSRC_simulation().run(vacancies=vacanciestable, history=eventhistory, gcs=self.gcs, jobs=self.jobs, hhs=self.hhs, data_objects=self.resources,\
#                dbcon=Con, variables=variables, years=years, debuglevel=debuglevel)
        Con.close_connection()

if __name__ == "__main__":
    # run estimation for the given variables
    variables = ("cost_to_income_ratio","income_and_ln_improvement_value_per_unit", \
            "ln_residential_units_within_walking_distance",\
            "percent_high_income_households_within_walking_distance_if_high_income",\
            "percent_low_income_households_within_walking_distance_if_low_income",\
            "percent_mid_income_households_within_walking_distance_if_mid_income", \
            "percent_minority_households_within_walking_distance_if_minority",\
            "percent_minority_households_within_walking_distance_if_not_minority",\
            "residential_units_when_household_has_children",\
            "young_household_in_high_density_residential",\
            "utility_for_SOV",\
            "same_household_age_in_faz",\
            "utility_for_transit_walk_0_cars",\
            "young_household_in_mixed_use",\
            "utility_for_transit_walk_1_person")
    coefficients = variables # or put your own names for coefficients here (as a tuple)
                             # in the same order as 'variables' 
    sim = Run_PSRCsimulation(variables=variables, coefficients=coefficients, debuglevel=4) 

