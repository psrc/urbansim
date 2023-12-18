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
from scipy.stats import scoreatpercentile
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache

class TestModel(Model):
    """Executes experimental code.
    """
    model_name = "Test Model"

    def run(self):
        """Runs the test model. 
        """

        dataset_pool = SessionConfiguration().get_dataset_pool()

        building_set = dataset_pool.get_dataset('building')

        res_unit_price = building_set.compute_variables('safe_array_divide(building.improvement_value*1.0, building.residential_units)')

        nonres_unit_price = building_set.compute_variables('safe_array_divide(building.improvement_value*1.0, building.non_residential_sqft)')

        building_set.add_primary_attribute(name='unit_price_residential', data=res_unit_price)

        building_set.add_primary_attribute(name='unit_price_non_residential', data=nonres_unit_price)

        cache_dir = SimulationState().get_cache_directory(); logger.log_status("cache_dir %s" % cache_dir)

        attribute_cache = AttributeCache(); logger.log_status("attribute_cache %s" % attribute_cache)

        #building_set = dataset_pool.get_dataset('building')
        
        #household_income = household_set.get_attribute("income")
        
        #logger.log_status("25th percentile %s" % scoreatpercentile(household_income,25))
        
        #logger.log_status("50th percentile %s" % scoreatpercentile(household_income,50))
        
        #logger.log_status("75th percentile %s" % scoreatpercentile(household_income,75))
        
        #household_zonetype = household_set.compute_variables("((household.zone_id * 100) + (household.building_type_id)).astype('i4')")
        
        #building_zonetype = building_set.compute_variables("((building.zone_id * 100) + (building.building_type_id)).astype('i4')")
        
        #household_set.add_primary_attribute(name='zonetype', data=household_zonetype)
        
        #building_set.add_primary_attribute(name='zonetype', data=building_zonetype)
        
        
        
        #household_county = household_set.compute_variables("household.disaggregate(building.disaggregate(parcel.county_id))")

        #household_set.add_primary_attribute(name='county', data=household_county)
        
        #household_county2 = household_set.compute_variables("((household.county>-1)*(household.county) + (household.county==-1)*0).astype('i4')")


        
        #building_county = building_set.compute_variables("building.disaggregate(parcel.county_id)")

        #building_set.add_primary_attribute(name='county', data=building_county)
        
        #household_tract = household_set.compute_variables("((household.tract10>0)*(household.tract10 - 6000000000)).astype('i4')")

        #household_set.add_primary_attribute(name='tract', data=household_tract)
        
        #building_tract = building_set.compute_variables("((building.tract10>0)*(building.tract10 - 6000000000)).astype('i4')")

        #building_set.add_primary_attribute(name='tract', data=building_tract)
        
        #household_tract = household_set.compute_variables('household.disaggregate(building.tract10)')

        #household_set.add_primary_attribute(name='tract10', data=household_tract)

        # #logger.log_status("size: %s" % (nodes.size()))

        # #logger.log_status("id: %s" % (nodes.get_id_name()))

        # nodes.add_primary_attribute(name='streetfeet_halfmile', data=measure)  #indexing correct?  can I just add this like that?

        # #logger.log_status("attributes: %s" % (nodes.get_attribute_names()))

        # #logger.log_status("nodes summary: %s" % (nodes.summary()))

        # #num_nodes = nodes.size()

        # #dummy_accvar = ones(num_nodes, dtype=int)

        # node_ids = nodes.get_id_attribute()

        # node_d = dict(zip(d['nodeids'],range(len(node_ids)))) #range starts at zero, should this be range + 1?
        # node_ids = [node_d[x] for x in node_ids]  # I dont quite understand this.  Execute this program line by line in IDLE and really understand the code

        # node_ids = array(node_ids, dtype="int") #wait, what?  We just replaced the above lines with a simple, sequential array.  

        # #logger.log_status("node ids: %s" % (node_ids))

        # #pya.initializeAccVars(1)

        # #pya.initializeAccVar(0,node_ids,node_resunits)

        # node_resunits = nodes.compute_variables('node.aggregate((building.residential_units*1.0*(building.residential_units>0)), intermediates=[parcel])')

        # node_avgfloors = nodes.compute_variables('node.aggregate((building.stories*1.0*(building.stories>0)), intermediates=[parcel],function=mean)')

        # node_avgyrbuilt = nodes.compute_variables('node.aggregate((building.year_built*1.0*(building.year_built>0)), intermediates=[parcel],function=mean)')

        # node_resunits = array(node_resunits, dtype="float32")

        # node_avgfloors = array(node_avgfloors, dtype="float32")

        # node_avgyrbuilt = array(node_avgyrbuilt, dtype="float32")

        # nodes.add_primary_attribute(name='resunits', data=node_resunits)

        # nodes.add_primary_attribute(name='avgfloors', data=node_avgfloors)

        # nodes.add_primary_attribute(name='avgyrbuilt', data=node_avgyrbuilt)

        # #logger.log_status("node resunits sum: %s" % (node_resunits.sum()))
        # #logger.log_status("node resunits shape: %s" % (node_resunits.shape))
        # #logger.log_status("node resunits size: %s" % (node_resunits.size))
        # #logger.log_status("node resunits: %s" % (node_resunits))

        # pya.initializeAccVars(3)

        # pya.initializeAccVar(0,node_ids,node_resunits)
        # pya.initializeAccVar(1,node_ids,node_avgfloors)
        # pya.initializeAccVar(2,node_ids,node_avgyrbuilt)

        # result_resunits=pya.getAllAggregateAccessibilityVariables(500,0,0,1,0)    #dist, varnum, aggtype (1 is avg),decaytype (use 2 when avg), impedance (use 0 for now unless differs by am/pm)

        # result_avgfloors=pya.getAllAggregateAccessibilityVariables(500,1,1,1,0)

        # result_avgyrbuilt=pya.getAllAggregateAccessibilityVariables(500,2,1,1,0)

        # #logger.log_status("result: %s" % (result_resunits))

        # #logger.log_status("result sum: %s" % (result_resunits.sum()))

        # nodes.add_primary_attribute(name='resunits_query', data=result_resunits)

        # nodes.add_primary_attribute(name='avgfloors_query', data=result_avgfloors)

        # nodes.add_primary_attribute(name='avgyrbuilt_query', data=result_avgyrbuilt)



  # # File "C:\opus\src\bayarea\test_model.py", line 65, in run
    # # pya.initializeAccVar(1,node_ids,node_resunits)
  # # File "C:\opus\src\bayarea\pyaccess.py", line 59, in initializeAccVar
    # # return _pyaccess.initialize_acc_var(cat,nodeids,accvar)
# # TypeError: array cannot be safely cast to required type

# # Assign land uses using the following two functions.  
# # First, you give it the number of categories. (i.e. employment by sector)
# # Then you assign the variable, passing the category and a set of floats that is the accessibility variable (e.g. population) that you want to assign to nodes.  You can have multiple assignments for a single node - imagine that you have population or square footage attached to parcels and that you're assigning these to nodes. 
   # # def initializeAccVars(my,numcategories):
       # # return _pyaccess.initialize_acc_vars(numcategories)

   # # def initializeAccVar(my,cat,nodeids,accvar):
       # # accvar, nodeids = my.sum_by_group(accvar, nodeids)
       # # return _pyaccess.initialize_acc_var(cat,nodeids,accvar)


