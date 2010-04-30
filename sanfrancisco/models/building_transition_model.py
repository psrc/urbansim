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
             new_building_copy_attrs,
             building_type_table,
             building_type_classification_table,
             vacancy_table,
             history_table,
             year,
             location_set,
             resources=None ):
        building_classes = building_type_classification_table.get_attribute("name")
        unit_attributes = building_type_classification_table.get_attribute('units')
        building_id_name = building_set.get_id_name()[0]
        location_id_name = location_set.get_id_name()[0]
        calc_attributes = [building_id_name, location_id_name, "year_built"]
        new_buildings   = {}
        for attribute in new_building_copy_attrs:
            new_buildings[attribute] = array([], dtype=building_set.get_data_type(attribute))
        for attribute in calc_attributes:
            new_buildings[attribute] = array([], dtype=building_set.get_data_type(attribute))
            
        # for convenience, make a map of building_type_id => (building_type)class_id
        # these names are hard-wired elsewhere
        building_type_id_to_class_id = {}
        building_type_ids = building_type_table.get_attribute("building_type_id")
        for idx in range(building_type_table.size()):
            building_type_id_to_class_id[building_type_ids[idx]] = \
                building_type_table.get_attribute("class_id")[idx]
        logger.log_status("building_type_id_to_class_id = " + str(building_type_id_to_class_id))
        
        # and make an column for the history table of the use classes
        history_use_classes = zeros( (history_table.size()), dtype=int8)
        history_uses = history_table.get_attribute("building_type_id")
        for idx in range(history_table.size()):
            history_use_classes[idx] = building_type_id_to_class_id[history_uses[idx]]
        logger.log_status("history_uses=" + str(history_uses))
        logger.log_status("history_use_classes=" + str(history_use_classes))

        max_id = building_set.get_id_attribute().max()
        new_building_id_start = max_id + 1
        new_building_id_end = max_id + 1
        building_set_size_orig = building_set.size()

        for itype in range(building_type_classification_table.size()): # iterate over building types
            building_class = building_classes[itype]
            building_class_id = building_type_classification_table.get_attribute("class_id")[itype]
            
            vacancy_attribute = 'target_total_%s_vacancy' % building_class.lower()
            if vacancy_attribute not in vacancy_table.get_known_attribute_names():
                logger.log_warning("No target vacancy for building class '%s' (e.g. no '%s' in target_vacancies). Transition model for this building class skipped." 
                                   % (building_class,vacancy_attribute)) 
                continue
            vacancy_table.get_attribute(vacancy_attribute)  # ensures that the attribute is loaded
            target_vacancy_rate = eval("vacancy_table.get_data_element_by_id( year ).%s" % vacancy_attribute)
            logger.log_status("Target vacancy rate for building_class %s is %f" % (building_class, target_vacancy_rate))

            compute_resources = Resources(resources)
            compute_resources.merge({"debug":self.debug})
            units_attribute         = unit_attributes[itype]
            occupied_sqft_attribute = 'occupied_sqft_of_typeclass_%s' % building_class.lower()
            total_sqft_attribute    = 'building_sqft'

            # determine current-year vacancy rates
            building_set.compute_variables(("sanfrancisco.building." + occupied_sqft_attribute,
                                            "sanfrancisco.building." + total_sqft_attribute), 
                                           resources = compute_resources)

            occupied_sqft_sum   = building_set.get_attribute(occupied_sqft_attribute).sum()
            total_sqft_sum      = float( building_set.get_attribute(total_sqft_attribute).sum() )
            occupancy_rate      = self.safe_divide(occupied_sqft_sum, total_sqft_sum)
            # cap it at 1.0
            if occupancy_rate > 1.0: occupancy_rate = 1.0
            vacancy_rate        = 1.0 - occupancy_rate
            vacant_sqft_sum     = vacancy_rate * total_sqft_sum

            should_develop_sqft = vacant_sqft_sum < (target_vacancy_rate*total_sqft_sum)
            logger.log_status("%s: vacancy rate: %4.2f   occupancy rate: %4.2f" 
                              % (building_class, vacancy_rate, occupancy_rate))
            logger.log_status("%s: vacant: %d, should be vacant: %f, sum units: %d"
                          % (building_class, vacant_sqft_sum, target_vacancy_rate*total_sqft_sum, total_sqft_sum))

            if not should_develop_sqft:
                logger.log_note(("Will not build any %s units, because the current vacancy of %d sqft\n"
                             + "is more than the %d sqft desired for the vacancy rate of %f.")
                            % (building_class,
                               vacant_sqft_sum,
                               target_vacancy_rate*total_sqft_sum,
                               target_vacancy_rate))
                continue

            #create buildings

            # find sample set of qualifying buildings in the events history, 
            # e.g. where the building_type is in the correct class, and a positive 
            # number of units or sqft (or whatever) were present
            history_values = history_table.get_attribute(units_attribute)
            index_sampleset = where( (history_values > 0) & (history_use_classes==building_class_id))[0]

            # Ensure that there are some development projects to choose from.
            logger.log_status("shape of index_sampleset=" + str(index_sampleset.shape))
            if index_sampleset.shape[0] == 0:
                logger.log_warning("Cannot create new buildings for building use class %s; no buildings in the event history table from which to sample."
                                   % building_class) 
                continue
            
            history_values_sampleset = history_values[index_sampleset]            
            logger.log_status("history_values_sampleset = " + str(history_values_sampleset))

            mean_size = history_values_sampleset.mean()
            idx = array( [] ,dtype="int32")
            #TODO: should the 'int' in the following line be 'ceil'?
            num_of_projects_to_select = max( 10, int( should_develop_units / mean_size ) )
            while True:
                idx = concatenate( ( idx, randint( 0, history_values_sampleset.size,
                                                   size=num_of_projects_to_select) ) )
                csum = history_values_sampleset[idx].cumsum()
                idx = idx[where( csum <= should_develop_units )]
                if csum[-1] >= should_develop_units:
                    break

            nbuildings = idx.size
            logger.log_status("idx = " + str(idx))

            new_building_id_end = new_building_id_start + nbuildings

            # copy_attributes
            for attribute in new_building_copy_attrs:
                attr_values = history_table.get_attribute(attribute)[index_sampleset[idx]]
                new_buildings[attribute] = concatenate((new_buildings[attribute], attr_values))
            
            # calc_attributes
            new_buildings[building_id_name] =concatenate((new_buildings[building_id_name], arange(new_building_id_start, new_building_id_end)))
            new_buildings[location_id_name] = concatenate((new_buildings[location_id_name], zeros(nbuildings)))
            new_buildings["year_built"] = concatenate((new_buildings["year_built"], year*ones(nbuildings)))
            logger.log_status("Creating %s %s of %s %s buildings." % (history_values_sampleset[idx].sum(),
                                                                      units_attribute, nbuildings, building_class))
            new_building_id_start = new_building_id_end + 1
            logger.log_status(new_buildings)
        building_set.add_elements(new_buildings, require_all_attributes=False)

        difference = building_set.size() - building_set_size_orig
        index = arange(difference) + building_set_size_orig
        return index
