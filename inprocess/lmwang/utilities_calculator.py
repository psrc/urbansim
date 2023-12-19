# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from numpy import newaxis, array, where, reshape, concatenate, arange, zeros, ones
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.specified_coefficients import SpecifiedCoefficients, SpecifiedCoefficientsFor1Submodel
from opus_core.coefficients import create_coefficient_from_specification, Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.linear_utilities import linear_utilities
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset
from urbansim.datasets.building_dataset import BuildingDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from opus_core.dataset_pool import DatasetPool
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from optparse import OptionParser
import re

def write_2d_data(data, header, filename):
    delimiter = ','
    nobs, alts, nvars = data.shape
    #ids = arange(nobs, shape=(nobs,1,1)) + 1
    #data = concatenate((ids, , data),axis=2)
    #nvars += 2
    nrows = nobs * alts
    #
    data = reshape(data,(-1,nvars))

    fh = open(filename,'w')
    fh.write(delimiter.join(header) + '\n')   #file header
    for row in range(nrows):
        line = [str(x) for x in data[row,]]
        fh.write(delimiter.join(line) + '\n')

    fh.flush()
    fh.close


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-m", "--model", dest="model", action="store", type="string",
                      help="model name")
    parser.add_option("-c", "--choice-set-name", dest="choice_set_name", action="store",
                      type="string", help="model name")
    parser.add_option("-d", "--cache-directory", dest="cache_directory", action="store",
                      type="string",  help="cache directory")
    parser.add_option("-b", "--base-year", dest="base_year", action="store", type="int",
                      default=2000, help="base year")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="end year")
    (options, args) = parser.parse_args()

    model = options.model
    choice_set_name = options.choice_set_name
    cache_directory = options.cache_directory
    base_year = options.base_year
    years = list(range(base_year, options.year+1))

    test_settings = {
                 'hlcm':{'specification_table':'household_location_choice_model_specification',
                         'coefficient_table':'household_location_choice_model_coefficients',
                         'agent_set_name':'household',
                         'agent_class':'from urbansim.datasets.household_dataset import HouseholdDataset',
                         'agent_attributes' : {'household_id':arange(1) + 1,
                                               'age_of_head':array([30]),
                                               'cars':array([1]),
                                               'children':array([0]),
                                               'income':array([56000]),
                                               'persons':array([2]),
                                               'race_id':array([1]),
                                               'workers':array([2]),
                                               'grid_id':(ones(1) * -1).astype("int32")
                                             },
                         'submodel_string':'urbansim.household.income'
                         },
                 'celcm':{'specification_table':'commercial_employment_location_choice_model_specification',
                         'coefficient_table':'commercial_employment_location_choice_model_coefficients',
                         'agent_set_name':'job',
                         'agent_class':'from urbansim.datasets.job_dataset import JobDataset',
                         'agent_attributes' : {'job_id':arange(13) + 1,
                                               'building_type':ones(13, dtype="int16"),
                                               'home_based':zeros(13, dtype="?"),
                                               'sector_id':arange(13) + 1,
                                               'grid_id':(ones(13) * -1).astype("int32")
                                               },
                         'submodel_string':'urbansim.job.sector_id'
                         },
                 'ielcm':{'specification_table':'industrial_employment_location_choice_model_specification',
                         'coefficient_table':'industrial_employment_location_choice_model_coefficients',
                         'agent_set_name':'job',
                         'agent_class':'from urbansim.datasets.job_dataset import JobDataset',
                         'agent_attributes' : {'job_id':arange(13) + 1,
                                               'building_type':ones(13, dtype="int16") + 2,  # industrial
                                               'home_based':zeros(13, dtype="?"),
                                               'sector_id':arange(13) + 1,
                                               'grid_id':(ones(13) * -1).astype("int32")
                                               },
                         'submodel_string':'urbansim.job.sector_id'
                         },
                 'hbelcm':{'specification_table':'home_based_employment_location_choice_model_specification',
                         'coefficient_table':'home_based_employment_location_choice_model_coefficients',
                         'agent_set_name':'job',
                         'agent_class':'from urbansim.datasets.job_dataset import JobDataset',
                         'agent_attributes' : {'job_id':arange(1) + 1,
                                               'building_type':ones(1, dtype="int16") + 3,
                                               'home_based':ones(1, dtype="?"),
                                               'sector_id':arange(1) + 1,
                                               'grid_id':(ones(1) * -1).astype("int32")
                                               },
                         'submodel_string':'urbansim.job.sector_id'
                         },
                 'rblcm':{'specification_table':'residential_building_location_choice_model_specification',
                         'coefficient_table':'residential_building_location_choice_model_coefficients',
                         'agent_set_name':'building',
                         'agent_class':'from urbansim.datasets.building_dataset import BuildingDataset',
                         'agent_attributes' : {'building_id':arange(7) + 1,
                                               'building_type_id':ones(7, dtype="16")*4, #residential
                                               'residential_units':array([1,2,3,5,10,20,30]),
                                               'sqft':zeros(7),
                                               'year_built':ones(7, dtype="int32")*base_year
                                               },
                         'submodel_string':'urbansim.building.size_category_residential'
                         },
                 'cblcm':{'specification_table':'commercial_building_location_choice_model_specification',
                         'coefficient_table':'commercial_building_location_choice_model_coefficients',
                         'agent_set_name':'building',
                         'agent_class':'from urbansim.datasets.building_dataset import BuildingDataset',
                         'agent_attributes' : {'building_id':arange(5) + 1,
                                               'building_type_id':ones(5, dtype="int16")*1, #commercial
                                               'residential_units':array([999, 1999, 4999, 9999, 100001]),
                                               'sqft':zeros(5),
                                               'year_built':ones(5, dtype="int32")*base_year
                                               },
                         'submodel_string':'urbansim.building.size_category_commercial'
                         },
                 'iblcm':{'specification_table':'industrial_building_location_choice_model_specification',
                         'coefficient_table':'industrial_building_location_choice_model_coefficients',
                                                  'agent_set_name':'building',
                         'agent_class':'from urbansim.datasets.building_dataset import BuildingDataset',
                         'agent_attributes' : {'building_id':arange(5) + 1,
                                               'building_type_id':ones(5, dtype="int16")*3, #industrial
                                               'residential_units':array([999, 1999, 4999, 9999, 100001]),
                                               'sqft':zeros(5),
                                               'year_built':ones(5, dtype="int32")*base_year
                                               },
                         'submodel_string':'urbansim.building.size_category_industrial'
                         },

                 'rdplcm':{'specification_table':'residential_development_location_choice_model_specification',
                           'coefficient_table':'residential_development_location_choice_model_coefficients',
                           'agent_set_name':'development_project',
                           'agent_class':'from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset',
                           'agent_attributes' : {'project_id':array([1,2,3,4,5,6,7]),
                                                 'residential_units':array([1,2,3,5,10,20,30]),
                                                 'grid_id':array([-1,-1,-1,-1,-1,-1,-1])
                                                 },
                           'submodel_string':'urbansim.development_project.size_category',
                           'categories':array([1,2,3,5,10,20]),
                           'what':'residential',
                           'attribute_name':'residential_units'
                         },
                 }

    try:
        agent_set_name = test_settings[model]['agent_set_name']
    except:
        raise UnImplmentedError("utilties caculation for %s hasn't been implemented." % model)

    file_name_root = os.path.join(cache_directory, 'diagnostic_data')

    if re.search('dplcm', model):  # if it is DPLCM
        exec(test_settings[model]['agent_class'], globals())
        agent_set = DevelopmentProjectDataset(categories=test_settings[model]['categories'],
                                                  what = test_settings[model]['what'],
                                                  attribute_name=test_settings[model]['attribute_name'],
                                                  data = test_settings[model]['agent_attributes'] )
    else:
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_dataset(
            Resources({'values': test_settings[model]['agent_attributes'],
                       'out_table_name':agent_set_name,
                } ) )
        exec("%s as AgentClass" % test_settings[model]['agent_class'], globals())
        agent_set = AgentClass( in_storage=storage, in_table_name=agent_set_name )

    if not os.path.exists(file_name_root):
        os.makedirs(file_name_root)

    SimulationState().set_cache_directory(cache_directory)
    SimulationState().set_current_time(base_year)

    SessionConfiguration(new_instance=True,
                         package_order=['psrc','urbansim','opus_core'],
                         in_storage=AttributeCache())

    submodel_string = test_settings[model]['submodel_string']
    from opus_core.variables.variable_name import VariableName
    from opus_core.variables.attribute_type import AttributeType
    submodel_string_short_name = VariableName(submodel_string).get_short_name()
    if submodel_string_short_name in agent_set.get_known_attribute_names():
        agent_set.add_attribute(agent_set.get_attribute(submodel_string_short_name), "submodel",
                                metadata=AttributeType.PRIMARY)
    else:
        agent_set.compute_variables("submodel = %s" % submodel_string)

    specification_table = test_settings[model]['specification_table']
    coefficients_table = test_settings[model]['coefficient_table']

    base_cache_storage = AttributeCache().get_flt_storage_for_year(base_year)
    specification = EquationSpecification(in_storage=base_cache_storage)
    specification.load(in_table_name=specification_table)
    coefficients = Coefficients(in_storage=base_cache_storage)
    coefficients.load(in_table_name=coefficients_table)
    specified_coefficients = SpecifiedCoefficients().create(coefficients, specification, neqs=1)
    variables = specified_coefficients.get_full_variable_names_without_constants()

    choice_filter_index = None #where(datasets[choice_set_name].get_attribute('zone_id') == 742)[0]

    for year in years:
        SimulationState().set_current_time(year)
        SessionConfiguration().get_dataset_pool().remove_all_datasets()
        dataset_pool = DatasetPool(
            package_order=['psrc','urbansim','opus_core'],
            storage=AttributeCache())

        choice_set = dataset_pool.get_dataset(choice_set_name)
        if choice_filter_index is None:
            choice_filter_index = arange(choice_set.size())
        specified_coefficients = SpecifiedCoefficients().create(coefficients, specification, neqs=choice_filter_index.size)
        interaction_dataset = InteractionDataset(dataset1=agent_set,
                                                 dataset2=dataset_pool.get_dataset(choice_set_name),
                                                 index1=None,
                                                 index2=choice_filter_index)

        interaction_dataset.compute_variables(variables,
                                              dataset_pool = dataset_pool)

        for index in range(agent_set.size()):
            submodel = agent_set.get_attribute('submodel')[index]
            if specified_coefficients.nsubmodels == 1:
                submodel = -2
            coef = SpecifiedCoefficientsFor1Submodel(specified_coefficients,submodel)
            data = interaction_dataset.create_logit_data(coef, index=array(index))
            coef_names = coef.get_coefficient_names_from_alt().tolist()
            ids = reshape(choice_set.get_id_attribute()[choice_filter_index], (1,choice_filter_index.size,1))
            write_2d_data(concatenate((ids, data),axis=2), ['id'] + coef_names, filename=os.path.join(file_name_root,
                                                                  '%s_data_submodel%sa%s_year%s.txt' % (model, submodel, index+1, year)))

            coef_values = coef.get_coefficient_values()
            utilities = linear_utilities().run(data, coef_values)
            write_2d_data(concatenate((ids,utilities[...,newaxis]),axis=2),['id','utilites'], filename=os.path.join(file_name_root,
                                                            '%s_utilities_submodel%sa%s_year%s.txt' % (model, submodel, index+1, year)))


