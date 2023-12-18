# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import numpy as np
from opus_core.session_configuration import SessionConfiguration
from opus_core.variables.variable_name import VariableName
from urbansim.models.transition_model import TransitionModel
from opus_core.datasets.dataset import DatasetSubset
from opus_core.logger import logger
from opus_core.sampling_toolbox import sample_noreplace

try:
    ## if installed, use PrettyTable module for status logging
    from prettytable import PrettyTable
except:
    PrettyTable = None

STEP_SIZE = 1.1
MAX_ITERATIONS = 50

class EstablishmentReappearanceModel(TransitionModel):
    """
    """
    
    model_name = "Establishment Reappearance Model"
    model_short_name = "ERM"
    
    def run(self, 
            year=None, 
            target_attribute_name='number_of_jobs', 
            sampling_filter="establishment.disappeared == 1", 
            reset_dataset_attribute_value={'disappeared':0, 'building_id':-1}, 
            dataset_pool=None,  
            **kwargs
            ):

        """         
        """

        id_name = 'control_total_id'
        ct_known_attributes = self.control_totals_all.get_primary_attribute_names()

        if target_attribute_name not in ct_known_attributes:
            raise AttributeError("Target attribute %s must be an attribute of control_total dataset" % target_attribute_name)
        
        if id_name not in ct_known_attributes:
            self.control_totals_all.add_attribute(name=id_name,
                                                  data = np.arange(1, self.control_totals_all.size()+1)
                                                  )
        if self.control_totals_all.get_id_name() != [id_name]:
            self.control_totals_all._id_names = [id_name]

        if year is None:
            year = SimulationState().get_current_time()
        this_year_index = np.where(self.control_totals_all['year']==year)[0]
        self.control_totals = DatasetSubset(self.control_totals_all, this_year_index)

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
                                  ] )
                           )
        column_names.sort(reverse=True)
        #column_values = dict([ (name, self.control_totals.get_attribute(name)) 
        #                       for name in column_names + [target_attribute_name]])

        self._code_control_total_id(column_names,
                                    dataset_pool=dataset_pool)
        
        target = self.control_totals[target_attribute_name]
        if self.dataset_accounting_attribute is None:
            self.dataset_accounting_attribute = '_one_'
            self.dataset.add_attribute(name = self.dataset_accounting_attribute,
                                       data = ones(self.dataset.size(), 
                                                   dtype=target.dtype))

        exp_actual = '_actual_ = control_total.aggregate(%s.%s)' % \
                        (self.dataset.dataset_name,
                         self.dataset_accounting_attribute)
        
        actual = self.control_totals_all.compute_variables(exp_actual,
                                    dataset_pool=dataset_pool)[this_year_index]
        actual = actual.astype(target.dtype)

        dataset_known_attributes = self.dataset.get_known_attribute_names() #update after compute

        #update control_total_id after removing disappeared
        column_names_new = list(set(column_names) - set(["disappeared"]))
        #self.control_totals_all.touch_attribute(target_attribute_name)
        self._code_control_total_id(column_names_new, 
                                    dataset_pool=dataset_pool)
        if sampling_filter:
            short_name = VariableName(sampling_filter).get_alias()
            if short_name not in dataset_known_attributes:
                filter_indicator = self.dataset.compute_variables(sampling_filter, dataset_pool=dataset_pool)
            else:
                filter_indicator = self.dataset[short_name]
        else:
            filter_indicator = 1

        to_reappear = np.array([], dtype=np.int32)
        #log header
        if PrettyTable is not None:
            status_log = PrettyTable()
            status_log.set_field_names(column_names + ["actual", "target", "difference", "action", "N", "note"])
        else:        
            logger.log_status("\t".join(column_names + ["actual", "target", "difference", "action", "N", "note"]))
            
        error_log = ''
        error_num = 1
        
        def log_status():
            ##log status
            action = "0"
            N = "0"
            if lucky_index is not None:
                if actual_num < target_num: 
                    action = "+" + str(action_num)
                    N = "+" + str(lucky_index.size)
                if actual_num > target_num: 
                    action = "-" + str(action_num)
                    N = "-" + str(lucky_index.size)
            
            cat = [ str(self.control_totals[col][index]) for col in column_names]
            cat += [str(actual_num), str(target_num), str(diff), action, N, error_str]
            if PrettyTable is not None:
                status_log.add_row(cat)
            else:
                logger.log_status("\t".join(cat))        

        for index, control_total_id in enumerate(self.control_totals.get_id_attribute()):
            target_num = target[index]
            actual_num = actual[index]
            action_num = 0
            n_num = 0
            diff = target_num - actual_num
            
            accounting = self.dataset[self.dataset_accounting_attribute]
            lucky_index = None
            error_str = ''
             
            if actual_num < target_num:

                indicator = self.dataset[id_name]==control_total_id
                n_indicator = indicator.sum()

                # do sampling from legitimate records
                legit_index = np.where(np.logical_and(indicator, filter_indicator))[0]
                legit_size = sum(accounting[legit_index])
                if legit_size > diff:  
                    ##there are more establishments that are marked as 'disappeared' than the gap between target and actual
                    ##sample required
                    mean_size = float(legit_size) / n_indicator if n_indicator != 0 else 1
                    n = int(np.ceil(diff / mean_size))

                    i = 0
                    while diff > 0 and action_num < diff:
                        if n > 1:  # adjust number of records to sample in each iteration
                            n = int( np.ceil((diff - action_num) / (mean_size * STEP_SIZE**i)) )
                        sampleable_index = legit_index[np.logical_not(np.in1d(legit_index, to_reappear))]
                        if n < sampleable_index.size:
                            lucky_index = sample_noreplace(sampleable_index, n)
                        else:
                            lucky_index = sampleable_index

                        temp_num = accounting[lucky_index].sum()
                        
                        if action_num + temp_num <= diff:
                            ## accept the last batch of samples only when it does not overshoot
                            to_reappear = np.concatenate((to_reappear, lucky_index))
                            action_num += temp_num
                        else:
                            ## already overshoot, reject the last batch and reduce the number of samples
                            i += 1
                        
                        if i > MAX_ITERATIONS:
                            ## we're in trouble
                            error_str = str(error_num)
                            error_log += "%s. We exhausted %s iterations and could not find samples to match target %s exactly.\n" % \
                                                                             (error_num, MAX_ITERATIONS, target_num)
                            error_num += 1
                            break
                elif 0 < legit_size <= diff:
                        # let all re-appear
                        lucky_index = legit_index
                        to_reappear = np.concatenate((to_reappear, lucky_index))
                        action_num += legit_size
                else:
                    error_str = str(error_num)
                    error_log += "%s. There is no suitable %s to sample from.\n" % (error_num, self.dataset.get_dataset_name())
                      #+ \ ','.join([col+"="+str(self.control_totals[col][index]) for col in column_names]) + '\n'
                    error_num += 1
            
            log_status()

        if PrettyTable is not None:
            logger.log_status("\n" + status_log.get_string() + '\n')
            
        if error_log:
            logger.log_error( '\n' + error_log)
        
        ## TODO: this sequence of add_elements first and then remove_elements works only when
        ## add_elements method appends data to the end of dataset and doesn't change the
        ## indices of existing elements.
        if to_reappear.size > 0:
            self._reset_attribute(self.dataset, 
                                 reset_attribute_dict = reset_dataset_attribute_value, 
                                 index=to_reappear)
           
        return self.dataset

