# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

#DISCLAIMER: THIS FILE IS OUT OF DATE AND NEEDS SIGNIFICANT MODIFICATIONS 
#            TO MAKE IT WORK

from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
from opus_core.equation_specification import EquationSpecification, load_specification_from_dictionary
from urbansim.datasets.household_dataset import HouseholdDataset
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
#from paris.paris_settings import ParisSettings
#from sandbox.estimator import Estimator
from urbansim.estimation.estimator import Estimator
from opus_core.resources import Resources
from opus_core.logger import logger
from numpy.random import seed
from opus_core.misc import unique
from numpy import arange, where, array, float32, concatenate
from time import time, localtime, strftime
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
import importlib


def compute_lambda(nbs):
        com_dept_id = nbs.get_attribute("dept")
        depts = unique(com_dept_id)
        unitsvac9 = []
        unitssec9 = []
        units9=[]
        stayers98 = []
        for d in depts:
                com_in_this_dept = where(com_dept_id==d)[0]
                unitsvac9.append(nbs.get_attribute("unitsvac9")[com_in_this_dept].sum())
                unitssec9.append(nbs.get_attribute("unitssec9")[com_in_this_dept].sum())
                units9.append(nbs.get_attribute("units9")[com_in_this_dept].sum())
                stayers98.append(nbs.get_attribute("stayers98")[com_in_this_dept].sum())
        
        unitsvac9 = array(unitsvac9)
        unitssec9 = array(unitssec9)
        units9 = array(units9)
        stayers98 = array(stayers98)

        movers98=units9 - stayers98 - unitssec9 - unitsvac9
        availableratio = unitsvac9 / units9.astype(float32)
        lambda_value = (units9 - unitssec9).astype(float32)/ (units9 - unitssec9 - unitsvac9) - unitsvac9.astype(float32) / movers98

        lambda_value = lambda_value * 0.9
        
        return (depts, lambda_value)

def compute_supply_and_vacancy_rate(nbs, depts, lambdas):
        com_dept_id = nbs.get_attribute("dept")

        unitssec9 = nbs.get_attribute("unitssec9")
        unitsvac9 = nbs.get_attribute("unitsvac9")
        units9 = nbs.get_attribute("units9")
        stayers98 = nbs.get_attribute("stayers98")
        
        movers98=units9 - stayers98 - unitssec9 - unitsvac9;
        nbs.add_attribute(movers98, 'movers')
        
        depts_list = depts.tolist()
        lambda_value = array([lambdas[depts_list.index(com)] for com in com_dept_id])
        
        supply = movers98 * lambda_value + unitsvac9
        vacancy_rate = 1 - movers98.sum() / float(supply.sum())
        if supply.sum() < movers98.sum():
                logger.log_error("total demand %s exceeds total supply %s " % (movers98.sum(), supply.sum()))
                raise ValueError
        return supply, vacancy_rate

        
def create_households_for_estimation(agent_set, dbcon):
        estimation_set = HouseholdDataset(in_storage=StorageFactory().get_storage('mysql_storage', storage_location=dbcon),
                in_table_name="households_for_estimation")
        agent_set.unload_primary_attributes()
        agent_set.load_dataset(attributes='*')
        estimation_set.load_dataset(attributes=agent_set.get_primary_attribute_names())
        for attr in agent_set.get_attribute_names():
            agent_set.attribute_boxes[attr].set_data(concatenate((estimation_set.attribute_boxes[attr].get_data(), agent_set.attribute_boxes[attr].get_data())))
        agent_set._update_id_mapping()
        agent_set.update_size()
        return (agent_set, arange(estimation_set.size()))

class HLCMEstimator(Estimator):

    def estimate(self, spec_var=None, spec_py=None,
            submodel_string = "workers", 
            agent_sample_rate=0.005, alt_sample_size=None):
        """

        """
        CLOSE = 0.001
        sampler = "opus_core.samplers.weighted_sampler"
        if alt_sample_size==None:
            sampler = None
        
        date_time_str=strftime("%Y_%m_%d__%H_%M", localtime())
        agent_sample_rate_str = "__ASR_" + str(agent_sample_rate)
        alt_sample_size_str = "_ALT_" + str(alt_sample_size)
        info_file = date_time_str + agent_sample_rate_str + alt_sample_size_str + "__info.txt"
        logger.enable_file_logging(date_time_str + agent_sample_rate_str + alt_sample_size_str + "__run.txt")
        logger.enable_memory_logging()
        logger.log_status("Constrained Estimation with agent sample rate of %s and alternatvie sample size %s\n" % \
                          (agent_sample_rate, alt_sample_size))
                
        t1 = time()
        
        SimulationState().set_current_time(2000)

        self.nbs = SessionConfiguration().get_dataset_from_pool("neighborhood")
        self.hhs = SessionConfiguration().get_dataset_from_pool('household')

        depts, lambda_value = compute_lambda(self.nbs)
        supply, vacancy_rate = compute_supply_and_vacancy_rate(self.nbs, depts, lambda_value)
        self.nbs.set_values_of_one_attribute("supply", supply)
        dataset_pool = SessionConfiguration().get_dataset_pool()
        dataset_pool.add_datasets_if_not_included({'vacancy_rate': vacancy_rate,
                                                   'sample_rate':agent_sample_rate
                                                   })
        SessionConfiguration()["CLOSE"] = CLOSE
        SessionConfiguration()['info_file'] = info_file
        
        if self.save_estimation_results:
            out_storage = StorageFactory().build_storage_for_dataset(type='sql_storage', 
                storage_location=self.out_con)
        
        if spec_py is not None:
            importlib.reload(spec_py)
            spec_var = spec_py.specification
        
        if spec_var is not None:
            self.specification = load_specification_from_dictionary(spec_var)
        else:
            in_storage = StorageFactory().build_storage_for_dataset(type='sql_storage', 
                storage_location=self.in_con)
            self.specification = EquationSpecification(in_storage=in_storage)
            self.specification.load(in_table_name="household_location_choice_model_specification")

        #submodel_string = "workers"
        
        seed(71) # was: seed(71,110)
        self.model_name = "household_location_choice_model"

        model = HouseholdLocationChoiceModelCreator().get_model(location_set=self.nbs, 
                                                                submodel_string=submodel_string,
                                                                sampler = sampler,
                                                                estimation_size_agents = agent_sample_rate * 100/20,    
                                                                # proportion of the agent set that should be used for the estimation,
                                                                # 
                                                                sample_size_locations = alt_sample_size,  # choice set size (includes current location)
                                                                compute_capacity_flag = True,
                                                                probabilities = "opus_core.mnl_probabilities",
                                                                choices = "urbansim.lottery_choices",
                                                                run_config = Resources({"capacity_string":"supply"}), 
                                                                estimate_config = Resources({"capacity_string":"supply","compute_capacity_flag":True}))

        #TODO: since households_for_estimation currently is the same as households, create_households_for_estimation
        #becomes unnecesarry
        #agent_set, agents_index_for_estimation  =  create_households_for_estimation(self.hhs, self.in_con)
        agent_set = self.hhs; agents_index_for_estimation = arange(self.hhs.size())
        self.result = model.estimate(self.specification, 
                                     agent_set=agent_set, 
                                     agents_index=agents_index_for_estimation, 
                                     debuglevel=self.debuglevel,
                                     procedure="urbansim.constrain_estimation_bhhh_two_loops" ) #"urbansim.constrain_estimation_bhhh"

        #save estimation results
        if self.save_estimation_results:    
            self.save_results(out_storage)
            
        logger.log_status("Estimation done. " + str(time()-t1) + " s")

if __name__ == "__main__":
    import sys

    try:agent_sample_rate = float(sys.argv[1])
    except:agent_sample_rate = 0.005

    try:alt_sample_size = int(sys.argv[2])
    except:alt_sample_size = None  #was 20 
    
    # run estimation for the given variables
    spec_var = {}
    spec_var = {
            -2: (
#            ("neighborhood.ln_residential_units","LLogRP99"),
            ("neighborhood.lpoprp99","lpoprp99"),                    
            ("paris.neighborhood.empscaled","empscaled"),
            ("paris.neighborhood.pop_density","pop_density"),
            ("paris.neighborhood.is_in_paris","paris"),                    
            ("paris.household_x_neighborhood.same_dept","same_dept"),
#            ("neighborhood.foreign_m","foreign_m"),
#            ("neighborhood.poor_m","poor_m"),
#            ("neighborhood.rich_m","rich_m"),
#            "paris.household_x_neighborhood.hhrich_nbpoor",
#            ("paris.household_x_neighborhood.hhrich_nbrich","hhrich_nbrich"),
            ("paris.household_x_neighborhood.hhpoor_nbpoor","hhpoor_nbpoor"),
            ("paris.household_x_neighborhood.hhnper1_nbnper1","hhnper1_nbnper1"),
            ("paris.household_x_neighborhood.hhnper2_nbnper2","hhnper2_nbnper2"),
            ("paris.household_x_neighborhood.hhnper3_nbnper3","hhnper3_nbnper3"),
            ("paris.household_x_neighborhood.hhnpam0_nbnpam0","hhnpam0_nbnpam0"),
            ("paris.household_x_neighborhood.hhnpam1_nbnpam1","hhnpam1_nbnpam1"),
            ("paris.household_x_neighborhood.hhnpam2_nbnpam2","hhnpam2_nbnpam2"),
            ("paris.household_x_neighborhood.hhyoung_nbyoung","hhyoung_nbyoung"),
            ("paris.household_x_neighborhood.hhforeign_nbforeign","hhforeign_nbforeign"),
            ("paris.household_x_neighborhood.hhfrench_nbforeign","hhfrench_nbforeign"),
            ("neighborhood.ln_price","ln_price"),
            ("paris.household_x_neighborhood.age_lnprice","age_lnprice"),
            ("paris.household_x_neighborhood.lninc_lnprice","lninc_lnprice"),
            ("paris.neighborhood.delta_pop","delta_pop"),
            ("neighborhood.rail9","rail"),
            ("neighborhood.subway","subway"),
            ("neighborhood.disthwy","disthwy"),
            ("neighborhood.tc","tc"),
            ("neighborhood.vp","vp"),
            ("paris.household_x_neighborhood.hhfem_nbtc","hhfem_nbtc")
            )
    }

    from .my_estimation_config import my_configuration    
    ss = SimulationState()
    ss.set_current_time(2000)
    ss.set_cache_directory(my_configuration['cache_directory'])

    attribute_cache = AttributeCache()
    sc = SessionConfiguration(new_instance=True,
                         package_order=my_configuration['dataset_pool_configuration'].package_order,
                         in_storage=attribute_cache)


    #settings = ParisSettings()
    #settings.prepare_session_configuration()
    estimator = HLCMEstimator(config=my_configuration,
                              save_estimation_results=False)

    #estimator = HLCMEstimator(settings=my_configuration, 
    #                    run_land_price_model_before_estimation=False, 
    #                    save_estimation_results=False, 
    #                    debuglevel=4)
    estimator.estimate(spec_var, agent_sample_rate=agent_sample_rate, alt_sample_size=alt_sample_size)

