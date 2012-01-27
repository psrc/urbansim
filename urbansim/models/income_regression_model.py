
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, exp, arange, zeros, where
from opus_core.resources import Resources
from opus_core.regression_model import RegressionModel
from opus_core.logger import logger
from urbansim.datasets.control_total_dataset import ControlTotalDataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.misc import unique
from opus_core.simulation_state import SimulationState

class IncomeRegressionModel(RegressionModel):
    """
    """
    model_name = "Income Regression Model"
    model_short_name = "IRM"

    def __init__(self, regression_procedure="opus_core.linear_regression", 
                 filter_attribute=None,
                 submodel_string=None, 
                 outcome_attribute=None,
                 run_config=None, 
                 estimate_config=None, 
                 debuglevel=0, dataset_pool=None):
        self.filter_attribute = filter_attribute
        if outcome_attribute is not None:
            self.outcome_attribute = outcome_attribute
        
        RegressionModel.__init__(self, 
                                 regression_procedure=regression_procedure, 
                                 submodel_string=submodel_string, 
                                 run_config=run_config, 
                                 estimate_config=estimate_config, 
                                 debuglevel=debuglevel, dataset_pool=dataset_pool)

    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None, 
             data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        """
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter_attribute <> None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index,
                                               dataset_pool=self.dataset_pool, resources=res)
        ##Initialize income of 2-person households that the hh-formation models have assigned a brand new household id.
        new_2household_ids = dataset.compute_variables('(household.income==(-2))')
        initialize_2income = where(new_2household_ids == 1)[0]
        if initialize_2income.size > 0:
            dataset.modify_attribute('income', dataset.compute_variables('(((household.workers)*18593) + ((household.aggregate(person.education, function=mean))*11293) +  ((household.aggregate(person.age, function=mean))*889) - 95508)')[initialize_2income], initialize_2income)
        ##Initialize income of 1-person households that the hh-dissolution models have assigned a brand new household id.
        new_1household_ids = dataset.compute_variables('(household.income==(-1))')
        initialize_1income = where(new_1household_ids == 1)[0]
        if initialize_1income.size > 0:
            dataset.modify_attribute('income', dataset.compute_variables('(((household.workers)*24000) + ((household.aggregate(person.education, function=mean))*5590) +  ((household.aggregate(person.age, function=mean))*583) - 51957)')[initialize_1income], initialize_1income)
        ##Initialize income of 3-person households that the hh-formation models have assigned a brand new household id.
        new_3household_ids = dataset.compute_variables('(household.income==(-3))')
        initialize_3income = where(new_3household_ids == 1)[0]
        if initialize_3income.size > 0:
            dataset.modify_attribute('income', dataset.compute_variables('(((household.workers)*20078) + ((household.aggregate(person.education, function=mean))*8531) +  ((household.aggregate(person.age, function=mean))*861) - 72319)')[initialize_3income], initialize_3income)
        ##Initialize income of 4-person households that the hh-formation models have assigned a brand new household id.
        new_4household_ids = dataset.compute_variables('(household.income==(-4))')
        initialize_4income = where(new_4household_ids == 1)[0]
        if initialize_4income.size > 0:
            dataset.modify_attribute('income', dataset.compute_variables('(((household.workers)*21883) + ((household.aggregate(person.education, function=mean))*9656) +  ((household.aggregate(person.age, function=mean))*1806) - 112131)')[initialize_4income], initialize_4income)
        ##Initialize income of 5-person households that the hh-formation models have assigned a brand new household id.
        new_5household_ids = dataset.compute_variables('(household.income==(-5))')
        initialize_5income = where(new_5household_ids == 1)[0]
        if initialize_5income.size > 0:
            dataset.modify_attribute('income', dataset.compute_variables('(((household.workers)*8797) + ((household.aggregate(person.education, function=mean))*9049) +  ((household.aggregate(person.age, function=mean))*670) - 27224)')[initialize_5income], initialize_5income)
        negative_income = dataset.compute_variables('household.income < 0')
        index_neg_inc = where(negative_income==1)[0]
        if index_neg_inc.size > 0:
            dataset.modify_attribute('income', zeros(index_neg_inc.size, dtype="int32"), index_neg_inc)
        #Run regression model- all coefficients are applied here except macro employment growth, which comes next
        incomes = RegressionModel.run(self, specification, coefficients, dataset, index, chunk_specification,
                                     run_config=run_config, debuglevel=debuglevel)
        #Add to the regression equation the term for employment growth (this year's jobs / last year's jobs).  Job totals from the control total dataset.
        # current_year = SimulationState().get_current_time()
        # if current_year == 2010:
            # term_to_add = 1.04*1.82 #322729 #319190.3
        # else:
            # base_year = '2009'
            # base_cache_storage = AttributeCache().get_flt_storage_for_year(base_year)
            # control_totals = ControlTotalDataset(in_storage=base_cache_storage, in_table_name="annual_employment_control_totals")
            # number_of_jobs = control_totals.get_attribute("number_of_jobs")
            # idx_current = where(control_totals.get_attribute("year")==current_year)[0]
            # jobs_current = number_of_jobs[idx_current]
            # idx_previous = where(control_totals.get_attribute("year")==(current_year-1))[0] 
            # jobs_previous = number_of_jobs[idx_previous]
            # emp_ratio = ((jobs_current.sum())*1.0)/(jobs_previous.sum())
            # logger.log_status("empratio:  %s" % (emp_ratio))
            # term_to_add = emp_ratio * 1.82
        # incomes = incomes + term_to_add
        incomes = exp(incomes)
        if (incomes == None) or (incomes.size <=0):
            return incomes
        if index == None:
             index = arange(dataset.size())
        dataset.set_values_of_one_attribute("income", incomes, index)
        #Bump up all negative incomes to zero
        negative_income = dataset.compute_variables('household.income < 0')
        index_neg_inc = where(negative_income==1)[0]
        if index_neg_inc.size > 0:
            dataset.modify_attribute('income', zeros(index_neg_inc.size, dtype="int32"), index_neg_inc)
        ##Add code to bump down all incomes above 3million
        too_high_income = dataset.compute_variables('household.income > 5000000')
        index_too_high_income = where(too_high_income==1)[0]
        if index_too_high_income.size > 0:
            dataset.modify_attribute('income', array(index_too_high_income.size*[5000000]), index_too_high_income)

        return

    def prepare_for_estimate(self, dataset=None, dataset_for_estimation_storage=None, dataset_for_estimation_table=None, join_datasets=False, **kwargs):
        from opus_core.model import get_specification_for_estimation
        from opus_core.datasets.dataset import Dataset
        spec = get_specification_for_estimation(**kwargs)
        if (dataset_for_estimation_storage is not None) and (dataset_for_estimation_table is not None):
            estimation_set = Dataset(in_storage = dataset_for_estimation_storage,
                                      in_table_name=dataset_for_estimation_table,
                                      id_name=dataset.get_id_name(), dataset_name=dataset.get_dataset_name())
            if join_datasets:
                dataset.join_by_rows(estimation_set, require_all_attributes=False,
                                    change_ids_if_not_unique=True)
                index = arange(dataset.size()-estimation_set.size(),dataset.size())
            else:
                index = dataset.get_id_index(estimation_set.get_id_attribute())
        else:
                index = None
        return (spec, index)
