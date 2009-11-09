# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter
from randstad.datasets.landuse_development_dataset import LandUseDevelopmentDataset
from urbansim.models.development_project_transition_model import DevelopmentProjectTransitionModel
from opus_core.model import Model
from opus_core.sampling_toolbox import probsample_replace
from opus_core.logger import logger
from numpy import arange, array, where, transpose, zeros, ones, float32, int32
from time import time

## TODO: Is this class working?
class DevelopmentTransitionModel( DevelopmentProjectTransitionModel ):
    """
    Creates land use developments for gridcells.  Refer to development_project_transition_model for more info.
    """
    def __init__( self, debuglevel=0 ):
        self.debug = DebugPrinter( debuglevel )
        self.model_name = "Landuse Development Transition Model"

    def run( self, vacancy_table, frequency_table, template_table, year, location_set, resources=None ):
        self.pre_check( location_set, vacancy_table, [] )
        target_residential_vacancy_rate = vacancy_table.get_data_element_by_id( year ).target_total_residential_vacancy
        target_non_residential_vacancy_rate = vacancy_table.get_data_element_by_id( year ).target_total_non_residential_vacancy
        compute_resources = Resources(resources)
#        compute_resources.merge({"household":household_set, "job":job_set, "debug":self.debug})
        location_set.compute_variables( ["urbansim.gridcell.vacant_residential_units",
                                        "urbansim.gridcell.vacant_commercial_sqft",
                                        "urbansim.gridcell.vacant_industrial_sqft"],
                                        resources = compute_resources )

        # determine current-year vacancy rates
        vacant_resunits_sum = location_set.get_attribute( "vacant_residential_units" ).sum()
        resunits_sum = float( location_set.get_attribute( "residential_units" ).sum() )
        vacant_residential_rate = self.safe_divide(vacant_resunits_sum, resunits_sum)

        vacant_commercial_sqft_sum = location_set.get_attribute( "vacant_commercial_sqft" ).sum()
        commercial_sqft_sum =  float( location_set.get_attribute( "commercial_sqft" ).sum() )
        vacant_commercial_rate =  self.safe_divide(vacant_commercial_sqft_sum, commercial_sqft_sum)

        vacant_industrial_sqft_sum = location_set.get_attribute( "vacant_industrial_sqft" ).sum()
        industrial_sqft_sum = float( location_set.get_attribute( "industrial_sqft" ).sum() )
        vacant_industrial_rate =  self.safe_divide(vacant_industrial_sqft_sum, industrial_sqft_sum)

        logger.log_status("Res: vacant res units: %d, should be vacant: %f, sum res units: %d"
                          % (vacant_resunits_sum, target_residential_vacancy_rate * resunits_sum, resunits_sum))
        logger.log_status("Com: vacant sqft: %d, should be vacant: %f, sum sqft: %d"
                          % (vacant_commercial_sqft_sum, target_non_residential_vacancy_rate * commercial_sqft_sum,
                             commercial_sqft_sum))
        logger.log_status("Ind: vacant sqft: %d, should be vacant: %f, sum sqft: %d"
                          % (vacant_industrial_sqft_sum, target_non_residential_vacancy_rate * industrial_sqft_sum,
                             industrial_sqft_sum))

        should_develop_resunits = max( 0, ( target_residential_vacancy_rate * resunits_sum - vacant_resunits_sum ) /
                                         ( 1 - target_residential_vacancy_rate ) )
        if not should_develop_resunits:
            logger.log_note(("Will not build any residential units, because the current residential vacancy of %d units\n"
                             + "is more than the %d units desired for the vacancy rate of %f.")
                            % (vacant_resunits_sum,
                               target_residential_vacancy_rate * resunits_sum,
                               target_residential_vacancy_rate))
        should_develop_commercial = max( 0, ( target_non_residential_vacancy_rate * commercial_sqft_sum - vacant_commercial_sqft_sum ) /
                                           ( 1 - target_non_residential_vacancy_rate ) )
        if not should_develop_commercial:
            logger.log_note(("Will not build any commercial sqft, because the current commercial vacancy of %d sqft\n"
                             + "is more than the %d sqft desired for the vacancy rate of %f.")
                            % (vacant_commercial_sqft_sum,
                               target_non_residential_vacancy_rate * commercial_sqft_sum,
                               target_non_residential_vacancy_rate))
        should_develop_industrial = max( 0, ( target_non_residential_vacancy_rate * industrial_sqft_sum - vacant_industrial_sqft_sum ) /
                                           ( 1 - target_non_residential_vacancy_rate ) )
        if not should_develop_industrial:
            logger.log_note(("Will not build any industrial sqft, because the current industrial vacancy of %d sqft\n"
                             + "is more than the %d sqft desired for the vacancy rate of %f.")
                            % (vacant_industrial_sqft_sum,
                               target_non_residential_vacancy_rate * industrial_sqft_sum,
                               target_non_residential_vacancy_rate))

#        projects = {}
#        should_develop = {"residential":should_develop_resunits,
#                          "commercial":should_develop_commercial,
#                          "industrial":should_develop_industrial}

#        average_improvement_value = {}
#        average_improvement_value["residential"] = self.safe_divide(
#            location_set.get_attribute("residential_improvement_value" ).sum(), resunits_sum)
#        average_improvement_value["commercial"] = self.safe_divide(
#            location_set.get_attribute("commercial_improvement_value" ).sum(), commercial_sqft_sum)
#        average_improvement_value["industrial"] = self.safe_divide(
#            location_set.get_attribute("industrial_improvement_value" ).sum(), industrial_sqft_sum)

        #create projects

        development_type_ids = []
        units = []; com_sqfts=[]; ind_sqfts=[]; gov_sqfts=[];
        while should_develop_resunits > 0 or should_develop_commercial > 0 or should_develop_industrial > 0:
            n = 1   # sample n developments at a time
            sampled_ids = probsample_replace(frequency_table.get_attribute('development_type_id'),
                                             n,
                                             frequency_table.get_attribute('frequency').astype(float32)/frequency_table.get_attribute('frequency').sum())
            for id in sampled_ids:
                index = where(template_table.get_attribute('development_type_id') == id)[0]
                res_unit = template_table.get_attribute_by_index('residential_units', index)
                com_sqft = template_table.get_attribute_by_index('commercial_sqft', index)
                ind_sqft = template_table.get_attribute_by_index('industrial_sqft', index)
                gov_sqft = template_table.get_attribute_by_index('governmental_sqft', index)

                should_develop_resunits -= res_unit[0]
                should_develop_commercial -= com_sqft[0]
                should_develop_industrial -= ind_sqft[0]

                development_type_ids.append(id)
                units.append(res_unit)
                com_sqfts.append(com_sqft)
                ind_sqfts.append(ind_sqft)
                gov_sqfts.append(gov_sqft)

        sizes = len(development_type_ids)
        if sizes > 0:
            storage = StorageFactory().get_storage('dict_storage')

            developments_table_name = 'developments'
            storage.write_table(
                    table_name=developments_table_name,
                    table_data={
                        "landuse_development_id": arange( sizes ),
                        "grid_id": -1 * ones( ( sizes, ), dtype=int32),
                        "development_type_id": array(development_type_ids),
                        "residential_units":array(units),
                        "commercial_sqft":array(com_sqfts),
                        "industrial_sqft":array(ind_sqfts),
                        "governmental_sqft":array(gov_sqfts),
                        "improvement_value": zeros( ( sizes, ), dtype="int32"),
                        },
                )

            developments = LandUseDevelopmentDataset(
                in_storage = storage,
                in_table_name = developments_table_name,
                )

        else:
            developments = None

        return developments
