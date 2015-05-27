# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, array, where, zeros, ones, logical_and, reshape, concatenate, clip, indices
from opus_core.ndimage import sum as ndimage_sum
from copy import copy
from urbansim.models.transition_model import TransitionModel
from opus_core.datasets.dataset import DatasetSubset
from opus_core.session_configuration import SessionConfiguration

class HHControlTotalsWithIncomeGrowth(TransitionModel):
    """
    The model updates the control totals table by increasing households' income by a given factor.
    It assumes that an ordinary transition model ran prior to this model. Thus, number of households 
    in each category match the control totals. In this model, households income is increased and the 
    number of households in each category defined in the control totals is computed. Then the control totals 
    table is updated with these counts.
    """
    model_name = "HHControlTotalsWithIncomeGrowth"
        
    def __init__(self, income_growth_factor, base_year, **kwargs):
        TransitionModel.__init__(self, **kwargs)
        self.income_growth_factor = income_growth_factor
        self.base_year = base_year
        
    def run(self, year, target_attribute_name="total_number_of_households", **kwargs):
        if year is not None:
            self.factor_exponent = year-self.base_year
            self._do_initialize_for_run(target_attribute_name)
            self._IGrun(year=year, target_attribute_name=target_attribute_name, **kwargs)
            self._update_dataset()
        self.control_totals_all.load_and_flush_dataset()
        
    def _update_dataset(self):
        self.dataset['income'] = self.orig_income

    def _do_initialize_for_run(self, target_attribute_name):
        new_income = self.dataset['income']*(self.income_growth_factor**self.factor_exponent)
        #new_income = self.dataset['income']*self.income_growth_factor
        self.orig_income = self.dataset['income'].copy()
        self.dataset['income'] = new_income
        if not "%s_orig" % target_attribute_name in self.control_totals_all.get_known_attribute_names():
            orig_values = self.control_totals_all.get_attribute(target_attribute_name).copy()
            self.control_totals_all.add_primary_attribute(data=orig_values,
                                                      name="%s_orig" % target_attribute_name)

    
    def _IGrun(self, year=None, target_attribute_name='number_of_households', dataset_pool=None):

        
        ## NOTE: always call compute_variables method on self.control_total_all instead of
        ## self.control_total, because there is a problem with DataSubset to handle index

        id_name = 'control_total_id'
        ct_known_attributes = self.control_totals_all.get_primary_attribute_names()

        if target_attribute_name not in ct_known_attributes:
            raise AttributeError, "Target attribute %s must be an attribute of control_total dataset" % target_attribute_name
        
        if id_name not in ct_known_attributes:
            self.control_totals_all.add_attribute(name=id_name,
                                                  data = arange(1, self.control_totals_all.size()+1)
                                                  )
        if self.control_totals_all.get_id_name() != [id_name]:
            self.control_totals_all._id_names = [id_name]

        if year is None:
            year = SimulationState().get_current_time()
        this_year_index = where(self.control_totals_all['year']==year)[0]
        self.control_totals = DatasetSubset(self.control_totals_all, this_year_index)
        dtype = self.control_totals_all[target_attribute_name].dtype
        if dataset_pool is None:
            try:
                dataset_pool = SessionConfiguration().get_dataset_pool()
            except AttributeError:
                dataset_pool = DatasetPool(datasets_dict={
                                           self.dataset.dataset_name:self.dataset,
                                           #sync_dataset.dataset_name:sync_dataset,
                                           'control_total': self.control_totals
                                            })
        column_names = list( set( ct_known_attributes  ) \
                           - set( [ target_attribute_name, 
                                   'year', 
                                   '_hidden_id_',
                                   id_name, 
                                   '_actual_',
                                   'sampling_threshold',
                                   'sampling_hierarchy',
                                   "%s_orig" % target_attribute_name
                                  ] )
                           )
        column_names.sort(reverse=True)
        self._code_control_total_id(column_names,
                                    dataset_pool=dataset_pool)
        
        if self.dataset_accounting_attribute is None:
            self.dataset_accounting_attribute = '_one_'
            self.dataset.add_attribute(name = self.dataset_accounting_attribute,
                                       data = ones(self.dataset.size(), 
                                                   dtype=dtype))

        exp_actual = '_actual_ = control_total.aggregate(%s.%s)' % \
                        (self.dataset.dataset_name,
                         self.dataset_accounting_attribute)
        
        actual = self.control_totals_all.compute_variables(exp_actual,
                                    dataset_pool=dataset_pool)[this_year_index]
        actual = actual.astype(dtype)

        self.control_totals_all.set_values_of_one_attribute(target_attribute_name, actual, index=this_year_index)
            
        return self.dataset    