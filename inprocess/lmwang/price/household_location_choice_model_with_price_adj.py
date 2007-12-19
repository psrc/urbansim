#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
from opus_core.misc import safe_array_divide, unique_values
from opus_core.datasets.dataset import Dataset
from numpy import allclose, alltrue, zeros, median, newaxis, concatenate, where
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory

class HouseholdLocationChoiceModelWithPriceAdj(HouseholdLocationChoiceModel):
    
    model_name = "Household Location Choice Model with Price Adjustment"
    model_short_name = "HLCM"
    
    def run_chunk(self, agents_index, agent_set, specification, coefficients):
        """
        This method overwrites the run_chunk method in LocationChoiceModel by introducing iterative adjustment
        to the unit_price attribute of choice_set according to its demand
        """
        CLOSE = 0.05
        maxiter = 30
        submarkets = self.define_submarket(submarket_id="urbansim_parcel.building.zone_id * 100 + building.building_type_id")
        capacity_string = self.capacity_string
        demand_string = self.run_config.get('demand_string', 'demand')
        
        ##set demand_string, so the demand for each submodel will be added as a choice_set attribute
        choices = HouseholdLocationChoiceModel.run_chunk(self, agents_index, agent_set, specification, coefficients)
        #upc = self.upc_sequence
        sdratio_submarket, sdratio_choice = self.compute_sdratio(submarkets, self.choice_set, capacity_string, demand_string)

        data_for_plot = {}
        data_for_plot['sdratio'] = sdratio_submarket[:, newaxis]
        data_for_plot['unit_price'] = self.choice_set.get_attribute("unit_price")[:, newaxis]
        
	for i in range(1, maxiter+1, 1):
	    submarkets_w_demand = where(submarkets.get_attribute('demand')>0)[0]
            logger.start_block("HLCM with bidding choice iteration %s" % i)
            logger.log_status("submarket sdratio:")
            self.log_descriptives(data_array=sdratio_submarket[submarkets_w_demand])
	    logger.log_status("building unit_price by building_type_id:")
            self.log_descriptives(dataset=self.choice_set, attribute='unit_price', by='building_type_id', 
				  show_values={4:'CONDO',12:'MFH',19:'SFH'})
	    logger.log_status("excess demand by building_type_id:")
            demand_submarket = submarkets.get_attribute('demand')
            demand_supply = demand_submarket - sdratio_submarket * demand_submarket
            w_excess_demand = where(demand_supply > 0)[0]
            submarket_building_type_id = submarkets.get_id_attribute() % 100
            self.log_descriptives(data_array=demand_supply[w_excess_demand],
                                  by=submarket_building_type_id[w_excess_demand], 
				  show_values={4:'CONDO',12:'MFH',19:'SFH'})
            
            #if allclose(sdratio_submarket, 1, atol=CLOSE):
            if alltrue(sdratio_submarket[submarkets_w_demand] > 1):
                logger.log_status("Convergence achieved.")
                break

            ##cap price adjustment to +/- 10%
            price_adj = 1 / sdratio_choice
            price_adj[price_adj == 0] = 1.0            
            price_adj[price_adj > 1.10] = 1.10
            price_adj[price_adj < 0.9] = 0.9
            
            unit_price = self.choice_set.get_attribute("unit_price")

            self.choice_set.set_values_of_one_attribute("unit_price", unit_price * price_adj)
            self.choice_set.set_values_of_one_attribute(demand_string, zeros(self.choice_set.size(), dtype="float32"))
            choices = HouseholdLocationChoiceModel.run_chunk(self, agents_index, agent_set, specification, coefficients)
            
            sdratio_submarket, sdratio_choice = self.compute_sdratio(submarkets, self.choice_set, capacity_string, demand_string)

            data_for_plot['sdratio'] = concatenate( (data_for_plot['sdratio'], sdratio_submarket[:,newaxis]), axis=1)
            data_for_plot['unit_price'] = concatenate( (data_for_plot['unit_price'], self.choice_set.get_attribute("unit_price")[:,newaxis]),
                                                       axis = 1)

            logger.end_block()
            
        self.plot_data(data_for_plot['sdratio'], main='sdratio_submkt')
        
        buiding_types = self.choice_set.get_attribute('building_type_id')
        data_for_plot['unit_price'] = concatenate( (self.choice_set.get_id_attribute()[:,newaxis], data_for_plot['unit_price'] ),
                                                   axis = 1)        
        for building_type in [4, 12, 19]:
            self.plot_data(data_for_plot['unit_price'][building_types==building_type,:],
                           main='unit_price_bldg_type_%s' % building_type )
        
        return choices

    def define_submarket(self, submarket_id):
        submarket_ids = self.choice_set.compute_variables("submarket_id=" + submarket_id)
        unique_submarket_ids = unique_values(submarket_ids)
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='submarkets', table_data={'submarket_id':unique_submarket_ids})
        submarkets = Dataset(in_storage=storage,
                             in_table_name='submarkets',
                             id_name='submarket_id',
                             dataset_name='submarket'
                             )
        return submarkets

    def compute_sdratio(self, submarkets, choice_set, capacity_string, demand_string):
        choice_submarket_id = choice_set.compute_variables("urbansim_parcel.%s.%s" % (choice_set.get_dataset_name(), submarkets.get_id_name()[0]))
        choice_submarket_index = submarkets.get_id_index( choice_submarket_id )
        supply = submarkets.sum_over_ids( choice_submarket_id, self.capacity )

        demand = submarkets.compute_variables("demand=submarket.aggregate(%s.%s)" % (choice_set.get_dataset_name(), demand_string) )
        ##TODO: an adjustment ratio should be included since this variable only represents the demand from agents in this chunk
        sdratio_submarket = safe_array_divide(supply, demand)
        
        return (sdratio_submarket, sdratio_submarket[choice_submarket_index] )

    def log_descriptives(self, data_array=None, dataset=None, attribute=None, by=None, show_values={}):
        if data_array is None:
            data_array=dataset.get_attribute(attribute)
        if by is None:
            logger.log_status("#N: %s\tmean: %.3f\tstd: %.3f" % (data_array.size, data_array.mean(), data_array.std()) )
            logger.log_status("min: %.3f\tmedian: %.3f\tmax: %.3f" % (data_array.min(), median(data_array), data_array.max()) )
        else:
	    #if type(by)==tuple:
		#by_value, show_values = by
	    #else:
		#by_value = by
		
            if type(by)==str:
		by_str = by
                by_value = dataset.get_attribute(by_str)
	    else:
		by_str = "" 
		by_value = by
	    
	    if show_values is None or show_values == {}:
		show_values = unique_values(by_value)
		
            assert(by_value.size==data_array.size)
            
            for item in show_values.iteritems():
		if type(item) == tuple:
		    value, description = item
		    description_str = "(%s)" % description
		else:
		    value = item
		    description_str = ""
                data = data_array[by_value==value]
                logger.log_status("%s %s%s:" % (by_str, value, description_str))
                logger.log_status("#N: %s\tmean: %.3f\tstd: %.3f" % (data.size, data.mean(), data.std()) )
                logger.log_status("min: %.3f\tmedian: %.3f\tmax: %.3f" % (data.min(), median(data), data.max()) )
                

    def plot_data(self, data_array, main, delimiter=','):
        #def _write_to_txt_file(self, data, header, input_file, delimiter='\t'):
        logger.start_block("Writing data to file " + main)
        newfile = open(main + '.csv', 'w')
        #newfile.write(delimiter.join(header) + "\n")
        rows, cols = data_array.shape
        for n in range(rows):
            newfile.write(delimiter.join([str(x) for x in data_array[n,]]) + "\n")
                                          
        newfile.close()
        logger.end_block()
