# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.opus_package_info import package
from numpy import where, array, ndarray, zeros, float32, resize
from numpy import ma
from opus_core.logger import logger
from opus_core.misc import clip_to_zero_if_needed

def attribute_label(dataset_name, attribute_name, pkg=None):
    if pkg is None:
        pkg = package().get_package_name()
    return pkg + '.' + dataset_name + '.' + attribute_name

def create_dependency_name_with_number(name, dataset_name, numbers):
    result = []
    from opus_core.variables.variable_family_name_translator import VariableFamilyNameTranslator
    translator = VariableFamilyNameTranslator()
    for i in numbers:
        new_name = translator.translate_family_name_into_instance_name(name, (i,))
        result.append(package().get_package_name() + "." +  dataset_name + "." + new_name)
    return result

def compute_lambda_for_vacancy(grouping_location_set, units_variable, vacant_units_variable, movers_variable,
                   secondary_residence_variable=None, multiplicator=1.0, resources=None):
        grouping_location_set.compute_variables([units_variable, vacant_units_variable, movers_variable], resources=resources)
        if secondary_residence_variable is not None:
            grouping_location_set.compute_variables([secondary_residence_variable], resources=resources)
            unitssecondary = grouping_location_set.get_attribute(secondary_residence_variable)
        else:
            unitssecondary = zeros(grouping_location_set.size())
        unitsvacant = grouping_location_set.get_attribute(vacant_units_variable)
        units = grouping_location_set.get_attribute(units_variable)
        movers = grouping_location_set.get_attribute(movers_variable)
        tsv = units - unitssecondary - unitsvacant
        lambda_value = ma.filled((units - unitssecondary).astype(float32)/ ma.masked_where(tsv==0, tsv),0) \
                            - ma.filled(unitsvacant.astype(float32) / ma.masked_where(movers==0, movers),0)
        lambda_value = lambda_value * multiplicator
        return lambda_value

def compute_supply_and_vacancy_rate(location_set, grouping_location_set, lambdas,
                                    vacant_units_variable, movers_variable, resources=None):
        grouping_id = location_set.get_attribute(grouping_location_set.get_id_name()[0])
        location_set.compute_variables([vacant_units_variable, movers_variable], resources=resources)
        unitsvacant = location_set.get_attribute(vacant_units_variable)
        movers = location_set.get_attribute(movers_variable)
        lambda_value = lambdas[grouping_location_set.get_id_index(grouping_id)]
        supply = movers * lambda_value + unitsvacant
        vacancy_rate = 1 - movers.sum() / float(supply.sum())
        if supply.sum() < movers.sum():
            logger.log_warning("Total demand %s exceeds total supply %s " % (movers.sum(), supply.sum()))
        return supply, vacancy_rate

def compute_supply_and_add_to_location_set(location_set, grouping_location_set, units_variable,
                                    vacant_units_variable, movers_variable, supply_attribute_name,
                                    secondary_residence_variable=None, multiplicator=1.0, resources=None):
    """All variable names are in fully-qualified form defined for the
    'location_set'. Their are aggregated for the grouping_location_set.
    'supply_attribute_name' is in a short form and will be added to the location_set.
    """
    aggregate_string = grouping_location_set.get_dataset_name() + ".aggregate(%s)"
    if secondary_residence_variable:
        gr_secondary_residence_variable = aggregate_string % secondary_residence_variable
    else:
        gr_secondary_residence_variable = None
    lambdas = compute_lambda_for_vacancy(grouping_location_set,
                                         aggregate_string % units_variable,
                                         aggregate_string % vacant_units_variable,
                                         aggregate_string % movers_variable,
                                         gr_secondary_residence_variable, multiplicator, resources)
    supply, dummy = compute_supply_and_vacancy_rate(location_set, grouping_location_set, lambdas,
                                    vacant_units_variable, movers_variable, resources)
    logger.log_status("lambda for estimating annual supply computed from:")
    logger.log_status("T: %s, V: %s, M: %s" % (units_variable, vacant_units_variable,
                                               movers_variable))
    if secondary_residence_variable:
        logger.log_status("S: %s" % secondary_residence_variable)
    location_set.add_primary_attribute(clip_to_zero_if_needed(supply, supply_attribute_name), supply_attribute_name)

from opus_core.tests import opus_unittest
class FunctionsTests(opus_unittest.OpusTestCase):
    def test_create_dependency_name_with_number(self):
        self.assertEqual(create_dependency_name_with_number('a_DDD_b', 'my_dataset', (1,2,3)),
                         ['urbansim.my_dataset.a_1_b',
                          'urbansim.my_dataset.a_2_b',
                          'urbansim.my_dataset.a_3_b'])

if __name__ == '__main__':
    opus_unittest.main()
