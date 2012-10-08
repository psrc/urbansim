# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import cPickle, time, sys, string, StringIO
#from bayarea.pyaccess import PyAccess
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy
from numpy import ones, array

class TestModel(Model):
    """Executes experimental code.
    """
    model_name = "Test Model"

    def run(self):
        """Runs the test model. 
        """
        dataset_pool = SessionConfiguration().get_dataset_pool()

        # building_set = dataset_pool.get_dataset('building')

        # parcel_set = dataset_pool.get_dataset('parcel')

        # btract = building_set.compute_variables('building.disaggregate(parcel.census_tract)')

        # building_set.add_primary_attribute(name='census_tract', data=btract)

        #household_res_type = household_set.get_attribute('residential_building_type_id')

        #index_update_building_type = where(household_res_type>0)[0]

        #household_set.modify_attribute('building_type_id', household_res_type[index_update_building_type], index_update_building_type)

        #household_set.modify_attribute('building_type_id', household_res_type)

        # if 'person_no' in person_set.get_known_attribute_names():
            # num_max_person_no = household_set.compute_variables('_num_max_person_no = household.aggregate(person.person_no == person.disaggregate(household.aggregate(person.person_no, function=maximum)))')
            # max_person_id = person_set.compute_variables('_max_person_id = person.person_id == person.disaggregate(household.aggregate(person.person_id, function=maximum))')
            # person_no_to_change = person_set.compute_variables('_to_change = person._max_person_id * person.disaggregate(household._num_max_person_no>1)')
            # index_to_change = where(person_no_to_change==1)[0]
            # if index_to_change.size > 0:
                # person_set.modify_attribute('person_no', person_set.get_attribute('person_no')[index_to_change] + 1, index_to_change)


        # res_unit_price = building_set.compute_variables('(building.building_type_id<5)*safe_array_divide(building.improvement_value, building.residential_units)')

        # nonres_unit_price = building_set.compute_variables('(building.building_type_id>6)*safe_array_divide(building.improvement_value, building.non_residential_sqft)')

        # building_set.add_primary_attribute(name='unit_price_residential', data=res_unit_price)

        # building_set.add_primary_attribute(name='unit_price_non_residential', data=nonres_unit_price)

        job_set = dataset_pool.get_dataset('job')

        household_set = dataset_pool.get_dataset('household')

        submarket_set = dataset_pool.get_dataset('submarket')

        employment_submarket_set = dataset_pool.get_dataset('employment_submarket')

        building_set = dataset_pool.get_dataset('building')

        building_set.add_attribute(name='employment_submarket', data=building_set.compute_variables('honolulu_parcel.building.employment_submarket_id'))

        building_set.add_attribute(name='submarket', data=building_set.compute_variables('honolulu_parcel.building.submarket_id'))

        job_submarket = job_set.compute_variables('job.disaggregate(building.employment_submarket)')

        household_submarket = household_set.compute_variables('household.disaggregate(building.submarket)')

        job_set.add_primary_attribute(name='employment_submarket_id', data=job_submarket)

        household_set.add_primary_attribute(name='submarket_id', data=household_submarket)

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


