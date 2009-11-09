# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter
from opus_core.variables.variable_name import VariableName
from opus_core.model import Model
from numpy.random import randint
from opus_core.logger import logger
from numpy import arange, array, where, zeros, ones, float32, int32, int8, concatenate

class BuildingTransitionModel( Model ):
    """
    Creates buildings of different building types, according to target_vacancies for each building type. The vacancy table
    must have attributes 'target_total_%s_vacancy' % type (e.g. target_total_residential_vacancy) for each building type
    that the transition model should run.
    """
    def __init__( self, debuglevel=0 ):
        self.debug = DebugPrinter( debuglevel )
        self.model_name = "Building Transition Model"

    def check_for_space( self, values ):
        """Check that this array of values sums to something > 0."""
        self.do_check( "x > 0", array( [sum( values )] ) )

    def check_target_vacancy_is_not_100_percent( self, value ):
        """Check that the target vacancy rate is not 100% (ratio == 1), because it doesn't make sense,
        and it also causes a divide by 0 error."""
        self.do_check( "x != 1", value )

    def safe_divide(self, numerator, denominator, return_value_if_denominator_is_zero=0, type=float):
        """If denominator == 0, return return_value_if_denominator_is_zero.
        Else return numerator / denominator.
        """
        if denominator == 0:
            return return_value_if_denominator_is_zero
        return type(numerator) / denominator

    def run( self, building_set,
#             building_use_table,
             building_use_classification_table,
             vacancy_table,
             history_table,
             year,
             location_set,
             resources=None ):
        building_classes = building_use_classification_table.get_attribute("name")
        unit_attributes = building_use_classification_table.get_attribute('units')
        building_id_name = building_set.get_id_name()[0]
        location_id_name = location_set.get_id_name()[0]
        new_buildings = {building_id_name: array([], dtype='int32'),
                         "building_use_id":array([], dtype=int8),
                         "year_built": array([], dtype='int32'),
#                         "building_sqft": array([], dtype='int32'),
#                         "residential_units": array([], dtype='int32'),
                         "unit_price": array([], dtype= float32),
                         location_id_name: array([], dtype='int32')}
        for attribute in unit_attributes:
            new_buildings[attribute] = array([], dtype='int32')

        max_id = building_set.get_id_attribute().max()
        new_building_id_start = max_id + 1
        new_building_id_end = max_id + 1
        building_set_size_orig = building_set.size()

        for itype in range(building_use_classification_table.size()): # iterate over building types
            building_class = building_classes[itype]
#            type_code = building_types_table.get_id_attribute()[itype]
            vacancy_attribute = 'target_total_%s_vacancy' % building_class
            if vacancy_attribute not in vacancy_table.get_known_attribute_names():
                logger.log_warning("No target vacancy for building class '%s'. Transition model for this building class skipped." % type)
                continue
            vacancy_table.get_attribute(vacancy_attribute)  # ensures that the attribute is loaded
            target_vacancy_rate = eval("vacancy_table.get_data_element_by_id( year ).%s" % vacancy_attribute)

            compute_resources = Resources(resources)
            compute_resources.merge({"debug":self.debug})
            units_attribute = unit_attributes[itype]
            vacant_units_attribute = 'vacant_%s_without_clip' % units_attribute

            # determine current-year vacancy rates
            building_set.compute_variables("sanfrancisco.building." + vacant_units_attribute,
                                           resources = compute_resources)

            vacant_units_sum = building_set.get_attribute(vacant_units_attribute).sum()
            units_sum = float( building_set.get_attribute(units_attribute).sum() )
            vacant_rate = self.safe_divide(vacant_units_sum, units_sum)

            should_develop_units = max( 0, ( target_vacancy_rate * units_sum - vacant_units_sum ) /
                                         ( 1 - target_vacancy_rate ) )
            logger.log_status(building_class + ": vacant units: %d, should be vacant: %f, sum units: %d"
                          % (vacant_units_sum, target_vacancy_rate * units_sum, units_sum))

            if not should_develop_units:
                logger.log_note(("Will not build any " + building_class + " units, because the current vacancy of %d units\n"
                             + "is more than the %d units desired for the vacancy rate of %f.")
                            % (vacant_units_sum,
                               target_vacancy_rate * units_sum,
                               target_vacancy_rate))
                continue

#            average_buildings_value = None
#            if (type+"_improvement_value") in location_set.get_known_attribute_names():
#                average_buildings_value = self.safe_divide(
#                    location_set.get_attribute(type+"_improvement_value" ).sum(), units_sum)

            #create buildings

            history_values = history_table.get_attribute(units_attribute)
            index_non_zeros_values = where( history_values > 0 )[0]
            history_values_without_zeros = history_values[index_non_zeros_values]
            history_type = history_table.get_attribute("building_use_id")
            history_type_without_zeros = history_type[index_non_zeros_values]
            history_price = history_table.get_attribute("unit_price")
            history_price_without_zeros = history_price[index_non_zeros_values]

            #TODO: what happens if history has only zeroes?
            mean_size = history_values_without_zeros.mean()
            idx = array( [] ,dtype="int32")
            # Ensure that there are some development projects to choose from.
            #TODO: should the 'int' in the following line be 'ceil'?
            num_of_projects_to_select = max( 10, int( should_develop_units / mean_size ) )
            while True:
                idx = concatenate( ( idx, randint( 0, history_values_without_zeros.size,
                                                   size=num_of_projects_to_select) ) )
                csum = history_values_without_zeros[idx].cumsum()
                idx = idx[where( csum <= should_develop_units )]
                if csum[-1] >= should_develop_units:
                    break

            nbuildings = idx.size

            for attribute in unit_attributes:

                #if attribute == units_attribute:
                    #new_unit_values = history_values_without_zeros[idx]
                #else:
                    #new_unit_values = zeros(nbuildings)
                #to accomodate mixed use buildings, allow non units_attribute to be non-zero
                new_unit_values = history_table.get_attribute(attribute)[index_non_zeros_values[idx]]

                new_buildings[attribute] = concatenate((new_buildings[attribute], new_unit_values))

            new_building_id_end = new_building_id_start + nbuildings
            new_buildings[building_id_name]=concatenate((new_buildings[building_id_name], arange(new_building_id_start, new_building_id_end)))
            new_buildings["building_use_id"] = concatenate((new_buildings["building_use_id"], history_type_without_zeros[idx]))
            new_buildings["year_built"] = concatenate((new_buildings["year_built"], year*ones(nbuildings)))
            new_buildings["unit_price"] = concatenate((new_buildings["unit_price"], history_price_without_zeros[idx]))
            new_buildings[location_id_name] = concatenate((new_buildings[location_id_name], zeros(nbuildings)))
            logger.log_status("Creating %s %s of %s %s buildings." % (history_values_without_zeros[idx].sum(),
                                                                      units_attribute, nbuildings, building_class))
            new_building_id_start = new_building_id_end + 1
            
        building_set.add_elements(new_buildings, require_all_attributes=False)

        difference = building_set.size() - building_set_size_orig
        index = arange(difference) + building_set_size_orig
        return index
