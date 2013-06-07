# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.choice_model import ChoiceModel
from opus_core.model import prepare_specification_and_coefficients
from opus_core.model import get_specification_for_estimation
from numpy import array, arange, where, ones, concatenate, logical_and, zeros
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace
from opus_core.misc import unique
from opus_core.logger import logger
from opus_core.models.model import prepare_for_estimate as default_prepare_for_estimate

class TenureChoiceModel2(ChoiceModel):
    """
    This predicts the probability of renting vs owning
    """
    model_name = "Tenure Choice Model"
    model_short_name = "TCM"

    def prepare_for_estimate(self, *args, **kwargs):
        return prepare_for_estimate(*args, **kwargs)
    
def prepare_for_estimate(household_set=None,
                         households_for_estimation_table=None,
                         agents_for_estimation_storage=None,
                         agents_for_estimation_table=None,
                         join_datasets=False,
                         *args, **kwargs):

    hh_estimation_set = None
    if households_for_estimation_table is not None:
        hh_estimation_set = Dataset(in_storage = agents_for_estimation_storage, 
                                 in_table_name=households_for_estimation_table,
                                 id_name=household_set.get_id_name(), 
                                 dataset_name=household_set.get_dataset_name())
        if join_datasets:
            household_set.join_by_rows(hh_estimation_set, 
                                       require_all_attributes=False,
                                       change_ids_if_not_unique=True)

    specification, index =  default_prepare_for_estimate(agents_for_estimation_storage=agents_for_estimation_storage,
                                                 agents_for_estimation_table=agents_for_estimation_table,
                                                 join_datasets=join_datasets,
                                                 *args, **kwargs)
    return (specification, index)

