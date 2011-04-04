# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
import re, copy
from numpy.lib.type_check import asscalar
from numpy import array, asarray, where, ones, zeros, ones_like 
from numpy import arange, concatenate, resize, int32, float64
from numpy import asscalar, setdiff1d, ceil, logical_and, logical_not
from numpy import searchsorted, argsort
from opus_core import ndimage
from opus_core.misc import ismember, unique
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.sampling_toolbox import sample_noreplace, sample_replace
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.datasets.dataset import DatasetSubset


try:
    ## if installed, use PrettyTable module for status logging
    from prettytable import PrettyTable
except:
    PrettyTable = None

STEP_SIZE = 1.1
MAX_ITERATIONS = 50
    
class TransitionModel(Model):
    """ 
    A generic transition model that clones or removes records from dataset to 
    fit distributions specified in control_total table.
        
    """
    
    model_name = "Transition Model"
    model_short_name = "TM"
    
    def __init__(self, dataset, 
                 dataset_accounting_attribute=None,
                 control_total_dataset=None, 
                 model_name=None, 
                 model_short_name=None,
                 **kwargs):
        """
        **Parameters**
        
                **dataset** : OPUS Dataset object, required
                
                        The main dataset whose records are to be sampled or removed.
                        
                **dataset_accounting_attribute** : string, optional
                        
                        Name of dataset attribute that represents quantities summing
                        toward target_attribute.  If unspecified, counting number of
                        dataset records and comparing it against target.
                        
                **control_total_dataset** : OPUS Dataset object, optional
                
                        Control_total dataset.  It can be loaded by prepare_for_run
                        method instead.
                        
                **model_name** : string, optional
                
                        Name of instantiated model. Default to "Transition Model"
                        
                **model_short_name** : string, optional
                        
                        Short name of instantiated model. Default to "TM"                         
                          
        """
        self.dataset = dataset
        self.dataset_accounting_attribute = dataset_accounting_attribute
        self.control_totals_all = control_total_dataset
        self.control_totals = control_total_dataset
        if model_name:
            self.model_name = model_name
        if model_short_name:
            self.model_short_name = model_short_name
    
    def _code_control_total_id(self, column_names, 
                               control_total_index=None,
                               dataset_pool=None):
        """
        Assigns a control_total_id to control_totals and self.dataset, so that
        they can be joined with each other for opus expression computation, e.g.
        "control_total.aggregate(household.age>65)".
        
        **Parameters**
        
                **column_names** : list, required
                
                        A list of column names that define a row in control total. 
                        Each of the names in the list must be a primary attribute
                        or a computable/computed attribute of both control_total 
                        and self.dataset.
                        
                **control_total_index** : array or integer, optional
                
                        Selectively only updates control_total_id row specified 
                        by control_total_index
        """
        
        id_name = 'control_total_id'
        assert id_name in self.control_totals.get_known_attribute_names()

        ct_known_attributes = self.control_totals_all.get_known_attribute_names()
        dataset_known_attributes = self.dataset.get_known_attribute_names()
        if id_name not in dataset_known_attributes:
            self.dataset.add_attribute(name=id_name,
                                       data = -1 * ones(self.dataset.size()))

        ## if no index is passed, reset all id_name attribute for dataset
        if control_total_index is None:
            control_total_index = arange(self.control_totals.size())
            self.dataset.modify_attribute(name=id_name,
                                          data=-1*ones(self.dataset.size()))
            
        if len(column_names) == 0:
            if len(control_total_index) == 1:
                control_total_id = resize(self.control_totals[id_name][control_total_index],
                                          self.dataset.size())
                self.dataset.modify_attribute(name=id_name,
                                              data=control_total_id)
            else:
                logger.log_error("")

            return 

        logger.be_quiet()
        expressions = []
        for column_name in column_names:
            ind_var = re.sub('_max$', '', re.sub('_min$', '', column_name))
             
            if   re.search('_min$', column_name):
                expressions.append( "(%s >= " % ind_var + "%" + "(%s)s)" % column_name )
            elif re.search('_max$', column_name):
                expressions.append( "(%s <= " % ind_var + "%" + "(%s)s)" % column_name )
            else:  
                expressions.append( "(%s == " % ind_var + "%" + "(%s)s)" % column_name )
                
            if column_name not in ct_known_attributes:
                ## we may need to compute a column in sampling_hierarchy
                self.control_totals_all.compute_one_variable_with_unknown_package(column_name, 
                                                     dataset_pool=dataset_pool)                
            if ind_var not in dataset_known_attributes:
                self.dataset.compute_one_variable_with_unknown_package(ind_var,
                                                                       dataset_pool=dataset_pool)
                
        for index in control_total_index:
            control_total_id = self.control_totals[id_name][index]
            ## parse expressions with column_name and column value
            expression_inst = '*'.join( [ expression % {column_name:self.control_totals[column_name][index]} \
                                        for expression, column_name in zip(expressions, column_names) 
                                        if self.control_totals[column_name][index] != -1] )
            
            ## TODO: handle -2 special value 
            is_this_id = self.dataset.compute_variables(expression_inst, quiet=True)
            self.dataset.modify_attribute(name=id_name, 
                                          data=control_total_id,
                                          index=where(is_this_id)[0])
            
        logger.talk()
        logger.log_status()
    
    def run(self, 
            year=None, 
            target_attribute_name='number_of_households', 
            sampling_threshold=0, 
            sampling_hierarchy=[], 
            sampling_filter="", 
            reset_dataset_attribute_value={}, 
            sync_dataset=None,
            reset_sync_dataset_attribute_value={}, 
            dataset_pool=None,  
            **kwargs
            ):
        """ 

        **Parameters**
        
                **year** : int, optional
                
                        Simulation year. If unspecified, gets value from SimulationState

                **target_attribute_name** : string, optional
                
                        Name of control total attribute that contains target values.                         

                **sampling_threshold** : int or string, optional
                 
                        Lower bound value or control total variable specifying whether
                        dataset records satifying conditions of a control total cell are 
                        suitable to be sampled. 

                **sampling_hierarchy** : list, optional
                 
                        A list of sampling hierarchy to traverse when sampling_threshold
                        isn't satified.
                        
                **sampling_filter** : string, optional
                 
                        Name of dataset attribute or variable indicating which 
                        records in dataset are eligible in the sampling for removal 
                        or cloning.

                **reset_dataset_attribute_value** : dictionary, optional
                 
                        Name of dataset attribute or variable indicating which 
                        records in dataset are eligible in the sampling for removal 
                        or cloning.                        

                **sync_dataset** : OPUS Dataset object, optional

                **reset_sync_dataset_attribute_value** : dictionary, optional

                **dataset_pool** : OPUS DatasetPool object, optional                                                        
        
        """
        
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
                                   'sampling_hierarchy'
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

        def get_threshold_val(threshold, dataset_pool=None):
            if not threshold:
                return None

            threshold_str = ''
            if type(threshold) == str:
                ## check if sampling_threshold is a number in str type
                try:
                    threshold = float(threshold)
                except ValueError:
                    threshold_str = threshold

            if type(threshold) in (int, float):
                threshold_str = '_actual_ > %s' % threshold

            if threshold_str:
                threshold_val = self.control_totals_all.compute_variables(threshold_str,
                                                                      dataset_pool=dataset_pool)

                return threshold_val
            else:
                import ipdb; ipdb.set_trace()
                error_msg = "Unknown sampling_threshold type; it must be of int, float, or str."
                logger.log_error(error_msg)
                raise TypeError, error_msg
        
        ## handle sampling_threshold and/or sampling_hierarchy specified in control_totals table
        threshold_ct = None; hierarchy_ct = None
        if 'sampling_threshold' in ct_known_attributes:
            threshold_ct = self.control_totals['sampling_threshold']
        if 'sampling_hierarchy' in ct_known_attributes:
            hierarchy_ct = self.control_totals['sampling_hierarchy']

        threshold_raw = sampling_threshold
        threshold_val = ones_like(actual)
        if sampling_threshold: 
            ## this has to computable
            threshold_val = get_threshold_val(threshold_raw, 
                                              dataset_pool=dataset_pool)[this_year_index]

        dataset_known_attributes = self.dataset.get_known_attribute_names() #update after compute
        
        if sampling_filter:
            short_name = VariableName(sampling_filter).get_alias()
            if short_name not in dataset_known_attributes:
                filter_indicator = self.dataset.compute_variables(sampling_filter, dataset_pool=dataset_pool)
            else:
                filter_indicator = self.dataset[short_name]
        else:
            filter_indicator = 1

        to_be_cloned = array([], dtype=int32)
        to_be_removed = array([], dtype=int32)
        #log header
        if PrettyTable is not None:
            status_log = PrettyTable()
            status_log.set_field_names(column_names + ["actual", "target", "difference", "action", "note"])
        else:        
            logger.log_status("\t".join(column_names + ["actual", "target", "difference", "action", "note"]))
            
        error_log = ''
        error_num = 1
        
        def log_status():
            ##log status
            action = "0"
            if lucky_index is not None:
                if actual_num < target_num: action = "+" + str(action_num)
                if actual_num > target_num: action = "-" + str(action_num)
            
            cat = [ str(self.control_totals[col][index]) for col in column_names]
            cat += [str(actual_num), str(target_num), str(diff), action, error_str]
            if PrettyTable is not None:
                status_log.add_row(cat)
            else:
                logger.log_status("\t".join(cat))        

        original_id = copy.copy(self.dataset[id_name])
        reset_hierarchy_value = {}
        for index, control_total_id in enumerate(self.control_totals.get_id_attribute()):
            indicator = original_id==control_total_id
            n_indicator = indicator.sum()

            target_num = target[index]
            actual_num = actual[index]
            action_num = 0
            diff = target_num - actual_num
            
            reset_hierarchy_attribute = False
            accounting = self.dataset[self.dataset_accounting_attribute]
            lucky_index = None
            error_str = ''
             
            if actual_num != target_num:
                
                if actual_num < target_num:
                    ## handle sampling_threshold and sampling_hierarchy
                    threshold_val_this = threshold_val[index]
    
                    ## sampling_threshold and sampling_hierarchy specified in control_totals 
                    ## override those passed in through arguments in configuration
                    threshold_raw_this = threshold_raw  # for logging
                    if threshold_ct is not None:
                        threshold_val_ct = get_threshold_val(asscalar(threshold_ct[index]),
                                                             dataset_pool=dataset_pool
                                                            )
                        if threshold_val_ct is not None:
                            threshold_raw_this = asscalar(threshold_ct[index])
                            threshold_val_this = threshold_val_ct[this_year_index][index]
    
                    hierarchy_this = sampling_hierarchy
                    if hierarchy_ct is not None:
                        hierarchy_list_ct = eval( hierarchy_ct[index] )  # assume to be a string of list, e.g. "['zone_id', 'raz_id']"
                        if hierarchy_list_ct:
                            hierarchy_this = hierarchy_list_ct
    
                    if not threshold_val_this:
                        if not hierarchy_this:
                            error_str = str(error_num)
                            error_log += "%s. Sampling_threshold %s is not reached and no sampling_hierarchy specified.\n" % \
                                         (error_num, threshold_raw_this)
                            error_num += 1
                            log_status()
                            continue  #TODO: shall we proceed to do sampling even if sampling_threshold is not satisfied
                                      #      and sampling_hierarchy is not specified? 
                        
                        #iterate sampling_hierarchy starting from the second element (index 1), because the first
                        #in hierarchy is the one supposed to be replaced 
                        i = 1 
                        while not threshold_val_this:
                            if i == len(hierarchy_this):
                                break
                            ##replace preceding sampling_threshold
                            column_names_new = list(set(column_names) \
                                                  - set(hierarchy_this[:i])) \
                                                  + [hierarchy_this[i]]
     
                            self._code_control_total_id(column_names_new, 
                                                        control_total_index=[index],
                                                        dataset_pool=dataset_pool)
                            threshold_val_this = get_threshold_val(threshold_raw_this,
                                                                   dataset_pool=dataset_pool
                                                                  )[this_year_index][index]
                            i += 1
    
                        if not threshold_val_this:
                            ## we have exhausted the sampling_hierarchy,
                            ## and yet the sampling_threshold is not reached
                            error_str = str(error_num)
                            error_log += "%s. Sampling_threshold %s is not reached after exhausting sampling_hierarchy: %s.\n" % \
                                              (error_num, threshold_raw_this, hierarchy_this)
                            error_num += 1
                            log_status()
                            continue  # TODO: shall we proceed to do sampling even if we exhaust sampling_hierarchy 
                                      #       and sampling_threshold is not satisfied? 
                        else:
                            error_str = str(error_num)
                            error_log += "%s. Sampling_threshold reached at sampling_hierarchy %s.\n" % \
                                                                             (error_num,
                                                                              hierarchy_this[i-1]
                                                                              )
                            error_num += 1
                            reset_hierarchy_attribute = True
                            indicator = self.dataset[id_name] == control_total_id
                            n_indicator = indicator.sum()
                
                
                legit_index = where(logical_and(indicator, filter_indicator))[0]
                if legit_index.size > 0:
                    abs_diff = abs(target_num - actual_num)
                    mean_size = float(sum(self.dataset[self.dataset_accounting_attribute][indicator])) \
                                                / n_indicator if n_indicator != 0 else 1
                    n = int(ceil(abs_diff / mean_size))
                    size_tbc_prev = to_be_cloned.size
                    i = 0
                    while diff > 0 and action_num < abs_diff:
                        if n > 1:
                            n = int( ceil((abs_diff - action_num) / (mean_size * STEP_SIZE**i)) )
                        lucky_index = sample_replace(legit_index, n)
                        temp_num = accounting[lucky_index].sum()
                        
                        if action_num + temp_num <= abs_diff:
                            ## accept the last batch of samples only when it does not overshoot
                            to_be_cloned = concatenate((to_be_cloned, lucky_index))
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

                    idx_to_be_cloned = arange(size_tbc_prev, \
                                              to_be_cloned.size)                    
                    ## TODO: for now, only reset hierarchy value if
                    ## the lowest hierarchy is a primary attribute of dataset
                    if reset_hierarchy_attribute and hierarchy_this[0] in \
                       self.dataset.get_primary_attribute_names():
                        h = hierarchy_this[0]
                        k = asscalar(self.control_totals[h][index])
                        
                        if reset_hierarchy_value.has_key(h):
                            if reset_hierarchy_value[h].has_key(k):
                                #concatenate
                                reset_hierarchy_value[h][k] = \
                                    concatenate((reset_hierarchy_value[h][k], 
                                                 idx_to_be_cloned))
                            else:
                                reset_hierarchy_value[h].update({k:idx_to_be_cloned})
                        else:
                            reset_hierarchy_value[h] = {k:idx_to_be_cloned}
                    
                    i = 0
                    while diff < 0 and action_num < abs_diff :
                        if n > 1:
                            n = int( ceil(( abs_diff - action_num) / (mean_size * STEP_SIZE**i)) )
                        legit_index_not_yet_sampled = setdiff1d(legit_index, to_be_removed)
                        lucky_index = sample_noreplace(legit_index_not_yet_sampled, n)
                        temp_num = accounting[lucky_index].sum()
                        
                        if action_num + temp_num <= abs_diff:
                            ## accept the last batch of samples only when it does not overshoot
                            to_be_removed = concatenate((to_be_removed, lucky_index))
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
                    
        self.post_run(self.dataset, to_be_cloned, to_be_removed, **kwargs)
        
        ## TODO: this sequence of add_elements first and then remove_elements works only when
        ## add_elements method appends data to the end of dataset and doesn't change the
        ## indices of existing elements.
        if to_be_cloned.size > 0:
            index_updated = self.dataset.duplicate_rows(to_be_cloned)
            self._reset_attribute(self.dataset, 
                                 reset_attribute_dict = reset_dataset_attribute_value, 
                                 index=index_updated)
            #reset hierarchy value
            for h, k in reset_hierarchy_value.items():
                for v, idx in k.items():
                    self._reset_attribute(self.dataset, 
                                          reset_attribute_dict={h:v},
                                          index=index_updated[idx])
            
            # sync with another dataset (duplicate matched records) after adding records to dataset
            # since we need to know new ids if they are changed.                    
            self.sync_datasets(sync_dataset=sync_dataset, 
                               add_index=to_be_cloned, 
                               new_id=self.dataset.get_id_attribute()[index_updated],
                               reset_sync_dataset_attribute_value=reset_sync_dataset_attribute_value)
        
        if to_be_removed.size > 0:
            #logger.log_status()
            # sync with another dataset (delete matched records) before removing records from dataset
            self.sync_datasets(sync_dataset=sync_dataset, remove_index=to_be_removed)
            self.dataset.remove_elements(to_be_removed)            
            
        return self.dataset
    
    def prepare_for_run(self, control_total_dataset_name=None, 
                        control_total_table=None, 
                        control_total_storage=None):
        """
        Loads control_total dataset.
        **Parameters**
        
                **control_total_dataset_name** : string, optional
                
                        Name of control_total dataset.
                        
                **control_total_table** : string, optional
                        
                        Table name of control_total dataset.
                        
                **control_total_storage** : OPUS Storage object, optional
                        
                        Storage that contains control total dataset.
                        
        """
        sc = SessionConfiguration()
        if (control_total_storage is None) or \
           ((control_total_table is None) and \
           (control_total_dataset_name is None)):
            dp = sc.get_dataset_pool()
            self.control_totals_all = dp.get_dataset( 'annual_%s_control_total' \
                                                      % self.dataset.get_dataset_name() )
        else:
            df = DatasetFactory()
            if not control_total_dataset_name:
                control_total_dataset_name = df.dataset_name_for_table(control_total_table)
            
            self.control_totals_all = df.search_for_dataset(control_total_dataset_name,
                                                        package_order=sc.package_order,
                                                        arguments={'in_storage':control_total_storage, 
                                                                   'in_table_name':control_total_table,
                                                                   'id_name':[]
                                                                   }
                                                        )

        self.control_totals_all.dataset_name = 'control_total'
    
    def post_run(self, *args, **kwargs):
        """ To be implemented in child class for additional function
        """
        pass
    
    def sync_datasets(self, sync_dataset=None, 
                      remove_index=None, 
                      remove_from_sync_dataset=True,
                      add_index=None, 
                      new_id=None, 
                      reset_sync_dataset_attribute_value={}):
        """ 
        Synchronizes sync_data with dataset.
        
        **Parameters**
                
                **sync_dataset** : OPUS Dataset object, optional
                
                **remove_index** : numpy array, optional
                
                        Index to self.dataset records to be removed 
                
                **remove_from_sync_dataset** : bool, optional
                        
                        Whether to remove from sync_dataset records that match
                        to remove_index. If not, flag these records with 
                        reset_sync_dataset_attribute_value.
                        
                **add_index** : numpy array, optional
                    
                        Index to self.dataset records to be cloned
                        
                **new_id** : numpy array, optional
                
                        New ids for sync_dataset when being cloned
                        
                **reset_sync_dataset_attribute_value**: dictionary, optional
                        
                        New attribute name and value for sync_dataset records that
                        are affected.
        
        """
        if sync_dataset is None:
            return
        
        #this may take a while
        logger.log_status("Synchronize %s dataset with %s dataset... " % \
                          ( sync_dataset.dataset_name,
                            self.dataset.dataset_name )
                         )

        dataset_id_name = self.dataset.get_id_name()[0]
        sync_dataset_id_name = sync_dataset.get_id_name()[0]
        known_attribute_names = sync_dataset.get_known_attribute_names()
        if dataset_id_name in known_attribute_names:
            # assume sync_dataset (n)-->(1) dataset, e.g. run TM on households and sync persons
            id_name_common = dataset_id_name
        elif sync_dataset_id_name in self.dataset.get_known_attribute_names():
            # assume dataset (n)-->(1) sync_dataset, e.g. e.g. run TM on persons and sync households (hypothetical example)
            id_name_common = sync_dataset_id_name
        else:
            ## there is no common id name to synchronize sync_dataset with dataset
            logger.log_error( "Dataset %s and %s have no common id field. Abort synchronizing these two datasets" % \
                             (self.dataset.get_dataset_name(), sync_dataset.get_dataset_name()) )
            return
        
        id_dataset = self.dataset[id_name_common]; id_sync_dataset = sync_dataset[id_name_common]
        if remove_index is not None and remove_index.size>0:
            index_sync_dataset = where( ismember(id_sync_dataset, id_dataset[remove_index]) )[0]
            if remove_from_sync_dataset: 
                sync_dataset.remove_elements(index_sync_dataset)
            else:
                self._reset_attribute(sync_dataset, 
                                     reset_attribute_dict = reset_sync_dataset_attribute_value, 
                                     index=index_sync_dataset)
            
        if add_index is not None and add_index.size>0:
            if new_id is not None: #need to duplicate rows of sync_dataset and update id of the duplicated rows
                assert new_id.size == add_index.size
                
                idx_sync_clone = array([], dtype=add_index.dtype)
                id_sync_clone = array([], dtype=new_id.dtype)
                ids = id_dataset[add_index]
                processed = zeros(ids.size, dtype='bool')
                uids, uidx = unique(ids, return_index=True)
                while not all(processed):
                    idx_sort = argsort(uids)
                    to_be_cloned = where(ismember(id_sync_dataset, uids))[0]
                    idx_sync_clone = concatenate((idx_sync_clone, to_be_cloned))
                    ss = uids[idx_sort].searchsorted(id_sync_dataset[to_be_cloned])
                    id_sync_clone = concatenate((id_sync_clone, new_id[uidx][idx_sort][ss]))
                    processed[uidx] = 1
                    uids, uidx = unique(ids[logical_not(processed)], 
                                        return_index=True)
                    uidx = arange(ids.size)[logical_not(processed)][uidx]
                    
                index_sync_dataset_updated = sync_dataset.duplicate_rows(idx_sync_clone)
                sync_dataset.modify_attribute(name=id_name_common, data=id_sync_clone, index=index_sync_dataset_updated)
       
            else:
                index_sync_dataset = where( ismember(id_sync_dataset, id_dataset[add_index]) )[0]
                index_sync_dataset_updated = sync_dataset.duplicate_rows(index_sync_dataset)

            self._reset_attribute(sync_dataset, 
                                 reset_attribute_dict = reset_sync_dataset_attribute_value, 
                                 index=index_sync_dataset_updated)
        
        ### TODO: where is the best location to flush sync_dataset
        ## leave the flushing to model_system for now
        #sync_dataset.flush_dataset()
        
    def _reset_attribute(self, dataset, reset_attribute_dict=None, index=None, add_unknown_attribute=False):
        """
        Resets Dataset attribute value for records indicated by index.

        **Parameters**
                
                **dataset** : Opus Dataset object, required
                        
                        dataset whose attributes are to be reset
                
                **reset_attribute_dict** : dictionary, optional
                        
                        dictionary with key being attribute name of dataset and
                        value being value of attribute to be set to        

                **index** : array, optional
                        
                        index of partial dataset attribute to be reset
        
        """
        if not reset_attribute_dict: return
        known_attribute_names = dataset.get_known_attribute_names()
        for key, value in reset_attribute_dict.items():
            if key in known_attribute_names:
                data_size = index.size if index is not None else dataset.size()
                data = resize(value, data_size)
                dataset.modify_attribute(name=key, data=data, index=index)
#                continue
#            
#            if index is not None: ## add attribute key whose value defaults to value
#                ## key is not a known attribute, but index is specified
#                self.dataset.compute_one_variable_with_unknown_package(key,
#                                                                       dataset_pool=dataset_pool)
#                result = self.dataset[key]
#                result[index] = value
            elif add_unknown_attribute:
                dataset.add_primary_attribute(data=resize(value, dataset.size()), name=key)

from opus_core.tests import opus_unittest
from opus_core.misc import ismember
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.resources import Resources
from numpy import array, logical_and, int32, int8, ma, all, allclose
from scipy import histogram
from opus_core.datasets.dataset import Dataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim_parcel.datasets.business_dataset import BusinessDataset
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.control_total_dataset import ControlTotalDataset
from urbansim.datasets.household_characteristic_dataset import HouseholdCharacteristicDataset

class Tests(opus_unittest.OpusTestCase):

    def setUp(self):
        #1) 6000 households with age_of_head < 50, income < 40,000, persons < 3.
        #2) 2000 households with age_of_head < 50, income < 40,000, persons >= 3.
        #3) 3000 households with age_of_head < 50, income >= 40,000, persons < 3.
        #4) 4000 households with age_of_head < 50, income >= 40,000, persons >= 3.
        #5) 2000 households with age_of_head >= 50, income < 40,000, persons < 3.
        #6) 5000 households with age_of_head >= 50, income < 40,000, persons >= 3.
        #7) 3000 households with age_of_head >= 50, income >= 40,000, persons < 3.
        #8) 8000 households with age_of_head >= 50, income >= 40,000, persons >= 3.

        self.households_data = {
            "household_id":arange(33000)+1,
            "grid_id": array(6000*[1] + 2000*[2] + 3000*[3] + 4000*[4] + 2000*[5] + 5000*[6] +
                                3000*[10]+ 8000*[100], dtype=int32),
            "age_of_head": array(6000*[40] + 2000*[45] + 3000*[25] + 4000*[35] + 2000*[50] + 5000*[60] +
                                3000*[75]+ 8000*[65], dtype=int32),
            "income": array(6000*[35000] + 2000*[25000] + 3000*[40000] + 4000*[50000] + 2000*[20000] +
                                5000*[25000] + 3000*[45000]+ 8000*[55000], dtype=int32),
            "persons": array(6000*[2] + 2000*[3] + 3000*[1] + 4000*[6] + 2000*[1] + 5000*[4] +
                                3000*[1]+ 8000*[5], dtype=int8),
            "mpa_id": array(11000*[1] + 4000 * [2] + 7000*[3] + 11000*[4])
            }
        
        import itertools
        total_persons = self.households_data['persons'].sum()
        self.persons_data = {
            "person_id":arange(total_persons)+1,
            "household_id": array( list(itertools.chain.from_iterable([[i] * p for i,p in zip(self.households_data['household_id'], self.households_data['persons'])])) ),
            ## head of the household is the oldest
            "age": array( list(itertools.chain.from_iterable([range(a, a-p*2, -2) for a,p in zip(self.households_data['age_of_head'], self.households_data['persons'])])) ),
            "job_id": zeros(total_persons)
            }

    def test_sampling_threshold(self):
        """ Test passing sampling_threshold through argument to run method:
            1. sampling_threshold = 6001,
            2. sampling_threshold = 'control_total.number_of_agents(household)>6001',
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "control_total_id": arange(1, 5),
            "age_of_head_min": array([ 50,  0,  50,  0]),
            "age_of_head_max": array([100, 49, 100, 49]),
            "persons_min":     array([  1,  1,   3,  3]),
            "persons_max":     array([  2,  2,   6,  6]),
            "total_number_of_households": array([16000, 26000, 16000, 26000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, 
                                      in_table_name='hct_set', 
                                      what='household', 
                                      id_name=['control_total_id'])
        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                           datasets_dict={'household':hh_set})
        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, 
                  target_attribute_name="total_number_of_households", 
                  sampling_threshold = 6001,
                  reset_dataset_attribute_value={'grid_id':-1})
        
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertArraysEqual(hct_set['households'], array([5000, 26000, 16000, 6000]))        
        
        #check that there are indeed 50000 total households after running the model
        #results = hh_set.size()
        #should_be = [50000]
        #self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
        #                 True, "Error, should_be: %s, but result: %s" % (should_be, results))
        model.run(year=2000, 
                  target_attribute_name="total_number_of_households", 
                  sampling_threshold = 'control_total.number_of_agents(household)>6001',
                  reset_dataset_attribute_value={'grid_id':-1})
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertArraysEqual(hct_set['households'], array([5000, 26000, 16000, 6000]))

    def test_sampling_hierarchy(self):
        """ Test passing sampling_threshold and sampling_hierarchy through 
            arguments to run method
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "control_total_id": arange(1, 5),
            "age_of_head_min": array([ 50,  0,  50,  0]),
            "age_of_head_max": array([100, 49, 100, 49]),
            "persons_min":     array([  1,  1,   3,  3]),
            "persons_max":     array([  2,  2,   6,  6]),
            "total_number_of_households": array([15000, 25000, 15000, 25000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=['control_total_id'])
        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                                   datasets_dict={'household':hh_set})
        
        ##code control_total on a sampling_hierarchy (not a primary attribute)        
        from urbansim.control_total.aliases import aliases as ct_aliases
        ct_aliases += ['persons_p2_max = control_total.persons_max + 2',
                       'persons_p4_max = control_total.persons_max + 4'
                       ]
        from urbansim.household.aliases import aliases as hh_aliases
        hh_aliases += ['persons_p2 = household.persons',
                       'persons_p4 = household.persons',
                       ]
                
        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, 
                  target_attribute_name="total_number_of_households", 
                  sampling_threshold = 6001,
                  sampling_hierarchy = ['persons_max', 'persons_p2_max', 'persons_p4_max'],
                  reset_dataset_attribute_value={'grid_id':-1},
                  dataset_pool=dataset_pool)
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        #self.assertArraysEqual(hct_set['households'], array([15000, 25000, 15000, 6000]))
        self.assertEqual(hct_set['households'].sum(), array([15000, 25000, 15000, 6000]).sum())

    def test_sampling_hierarchy_reset_primary_dataset_attribute(self):
        """ Test passing sampling_threshold and sampling_hierarchy through 
            arguments to run method
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "control_total_id": arange(1, 5),
            "mpa_id":     array([1,  2,  3,  4]),
           #"total_number_of_households": array([12000,  8000, 15000, 15000]),
           "total_number_of_households": array([10000, 10000, 15000, 15000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=['control_total_id'])
        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                                   datasets_dict={'household':hh_set})
        
        ##code control_total on a sampling_hierarchy (not a primary attribute)        
        from urbansim.control_total.aliases import aliases as ct_aliases
        ct_aliases += ['county_id = (mpa_id <= 2)*1 + (mpa_id >=3)*2',
                       'region_id = county_id * 0 + 1'
                       ]
        from urbansim.household.aliases import aliases as hh_aliases
        hh_aliases += ['county_id = (mpa_id <= 2)*1 + (mpa_id >=3)*2',
                       'region_id = county_id * 0 + 1'
                       ]
                
        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, 
                  target_attribute_name="total_number_of_households", 
                  sampling_threshold = 'control_total.number_of_agents(household)>15000',
                  sampling_hierarchy = ['mpa_id', 'county_id', 'region_id'],
                  reset_dataset_attribute_value={'grid_id':-1},
                  dataset_pool=dataset_pool)
        results = histogram(hh_set['mpa_id'], [1,2,3,4,4])[0]
        #self.assertEqual(results.sum(), array([12000, 8000, 15000, 15000]).sum())
        #self.assertEqual(results.sum(), array([10000, 10000, 15000, 15000]).sum())
        print results
        #self.assertArraysEqual(results, array([12000, 8000, 15000, 15000]))
        self.assertArraysEqual(results, array([10000, 10000, 15000, 15000]))
        
    def test_threshold_hierarchy_in_control_totals(self):
        """Test when sampling_threshold and sampling_hierarchy are provided in control totals
        instead of being passed through arguments of run method.
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "control_total_id": arange(1, 5),
            "age_of_head_min": array([ 50,  0,  50,  0]),
            "age_of_head_max": array([100, 49, 100, 49]),
            "persons_min":     array([  1,  1,   3,  3]),
            "persons_max":     array([  2,  2,   6,  6]),
            "sampling_threshold": array([6001, 6001, 6001, 6001]),
            "sampling_hierarchy": array(["['persons_max', 'persons_p2_max', 'persons_p4_max']",
                                         "['persons_max', 'persons_p2_max', 'persons_p4_max']",
                                         "['persons_max', 'persons_p2_max', 'persons_p4_max']",
                                         "['persons_max', 'persons_p2_max', 'persons_p4_max']",
                                        ]),
            "total_number_of_households": array([15000, 25000, 15000, 25000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', 
                            table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, 
                                      in_table_name='hct_set', 
                                      what='household', 
                                      id_name=['control_total_id'])
        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                           datasets_dict={'household':hh_set})
        ##code control_total on a sampling_hierarchy (not a primary attribute)        
        from urbansim.control_total.aliases import aliases as ct_aliases
        ct_aliases += ['persons_p2_max = control_total.persons_max + 2',
                       'persons_p4_max = control_total.persons_max + 4'
                       ]
        from urbansim.household.aliases import aliases as hh_aliases
        hh_aliases += ['persons_p2 = household.persons',
                       'persons_p4 = household.persons',
                       ]

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, 
                  target_attribute_name="total_number_of_households", 
                  #sampling_threshold = 6001,
                  #sampling_hierarchy = ['persons_max', 'persons_p2_max', 'persons_p4_max'],
                  reset_dataset_attribute_value={'grid_id':-1},
                  dataset_pool=dataset_pool)

        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertEqual(hct_set['households'].sum(), array([15000, 25000, 15000, 6000]).sum())
       
    def test_code_control_total_id(self):
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "control_total_id": arange(1, 5),
            "age_of_head_min": array([ 50,  0,  50,  0]),
            "age_of_head_max": array([100, 49, 100, 49]),
            "persons":         array([  1,  1,   2,  2]),
            "income_min":      array([  1,  1,   2,  2]),
            "income_max":      array([  1,  1,   2,  2]),
            "total_number_of_households": array([15000, 25000, 15000, 25000])
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=['control_total_id'])

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model._code_control_total_id(['age_of_head_min', 'age_of_head_max'])

        self.assert_(all(ismember(hh_set['control_total_id'], [-1, 3, 4])))
        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                                   datasets_dict={'household':hh_set})
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertArraysEqual(hct_set['households'], array([0, 0, 18000, 15000]))
        
        model._code_control_total_id(['age_of_head_min', 'age_of_head_max', 'persons'])
        self.assert_(all(ismember(hh_set['control_total_id'], [-1, 1, 2, 3, 4])))
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertArraysEqual(hct_set['households'], array([5000, 3000, 0, 6000]))
        
        ##code control_total on a sampling_hierarchy (not a primary attribute)        
        from urbansim.control_total.aliases import aliases as ct_aliases
        ct_aliases += ['person_ge2 = control_total.persons >= 2']
        from urbansim.household.aliases import aliases as hh_aliases
        hh_aliases += ['person_ge2 = household.persons >= 2']
        
        model._code_control_total_id(['age_of_head_min', 'age_of_head_max', 'person_ge2'], 
                                     control_total_index=[2], 
                                     dataset_pool=dataset_pool)
        self.assert_(all(ismember(hh_set['control_total_id'], [-1, 1, 2, 3, 4])))
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertArraysEqual(hct_set['households'], array([5000, 3000, 13000, 6000]))        

        model._code_control_total_id(['age_of_head_min', 'age_of_head_max'])
        self.assert_(all(ismember(hh_set['control_total_id'], [-1, 1, 2, 3, 4])))
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertArraysEqual(hct_set['households'], array([0, 0, 18000, 15000]))

        model._code_control_total_id(['age_of_head_min', 'age_of_head_max', 'person_ge2'], 
                                     control_total_index=[3],
                                     dataset_pool=dataset_pool)
        self.assert_(all(ismember(hh_set['control_total_id'], [-1, 1, 2, 3, 4])))
        hct_set.compute_variables('households=control_total.number_of_agents(household)', 
                                 dataset_pool=dataset_pool)
        self.assertArraysEqual(hct_set['households'], array([0, 0, 18000, 15000]))
        #                                  it is not  array([0, 0, 18000, 12000]
        # because only update control_total_id for passed index, in this case,
        # because index 3 (0-49, persons>2) is a smaller set than (0-49) computed
        # before this call of _code_control_total_id, thus there is no observed
        # change in control_total_id field of households
        

    def test_same_distribution_after_household_addition(self):
        """Using the control_totals and no marginal characteristics,
        add households and ensure that the distribution within each group stays the same
        """

        annual_household_control_totals_data = {
            "year": array([2000]),
            "total_number_of_households": array([50000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what="household", id_name="year")

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        #check that there are indeed 50000 total households after running the model
        results = hh_set.size()
        should_be = [50000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the number of unplaced households is exactly the number of new households created
        results = where(hh_set.get_attribute("grid_id")<=0)[0].size
        should_be = [17000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households in each group is the same as before running the model
        results = self.get_count_all_groups(hh_set)
        should_be = array([6000.0/33000.0*50000.0, 2000.0/33000.0*50000.0, 3000.0/33000.0*50000.0, 4000.0/33000.0*50000.0,
                     2000.0/33000.0*50000.0, 5000.0/33000.0*50000.0, 3000.0/33000.0*50000.0, 8000.0/33000.0*50000.0])
        self.assertEqual(ma.allclose(results, should_be, rtol=0.05),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        # check the types of the attributes
        self.assertEqual(hh_set.get_attribute("age_of_head").dtype, int32,
                         "Error in data type of the new household set. Should be: int32, is: %s" % str(hh_set.get_attribute("age_of_head").dtype))
        self.assertEqual(hh_set.get_attribute("income").dtype, int32,
                         "Error in data type of the new household set. Should be: int32, is: %s" % str(hh_set.get_attribute("income").dtype))
        self.assertEqual(hh_set.get_attribute("persons").dtype, int8,
                         "Error in data type of the new household set. Should be: int8, is: %s" % str(hh_set.get_attribute("persons").dtype))

    def test_same_distribution_after_household_subtraction(self):
        """Using the control_totals and no marginal characteristics,
        subtract households and ensure that the distribution within each group stays the same
        """
        annual_household_control_totals_data = {
            "year": array([2000]),
            "total_number_of_households": array([20000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what="household", id_name="year")

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        #check that there are indeed 20000 total households after running the model
        results = hh_set.size()
        should_be = [20000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households in each group is the same as before running the model
        results = self.get_count_all_groups(hh_set)
        should_be = [6000.0/33000.0*20000.0, 2000.0/33000.0*20000.0, 3000.0/33000.0*20000.0, 4000.0/33000.0*20000.0,
                     2000.0/33000.0*20000.0, 5000.0/33000.0*20000.0, 3000.0/33000.0*20000.0, 8000.0/33000.0*20000.0]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.05),
                         True, "Error, should_be: %s,\n but result: %s" % (should_be, results))

    def test_controlling_with_one_marginal_characteristic(self):
        """Using the age_of_head as a marginal characteristic, which would partition the 8 groups into two larger groups
        (those with age_of_head < 40 and >= 40), ensure that the control totals are met and that the distribution within
        each large group is the same before and after running the model
        """

        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "age_of_head_min": array([111, 101,  50,  0]),
            "age_of_head_max": array([120, 110, 100, 49]),
            "total_number_of_households": array([1, 1, 15000, 25000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=[])

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        #check that there are indeed 40000 total households after running the model
        results = hh_set.size()
        should_be = [40000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the total number of households within first four groups increased by 10000
        #and that the total number of households within last four groups decreased by 3000
        results = histogram(hh_set['age_of_head'], bins=[0, 49,100, 110, 120])[0]
        should_be = [25000, 15000, 0, 0]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households within groups 1-4 and 5-8 are the same before and after
        #running the model, respectively
        results = self.get_count_all_groups(hh_set)
        should_be = [6000.0/15000.0*25000.0, 2000.0/15000.0*25000.0, 3000.0/15000.0*25000.0, 4000.0/15000.0*25000.0,
                     2000.0/18000.0*15000.0, 5000.0/18000.0*15000.0, 3000.0/18000.0*15000.0, 8000.0/18000.0*15000.0]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.05),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def test_controlling_with_three_marginal_characteristics(self):
        """Controlling with all three possible marginal characteristics in this example, age_of_head, income, and persons,
        this would partition the 8 groups into the same 8 groups, and with a control total specified for each group, we must
        ensure that the control totals for each group exactly meet the specifications.
        """

        #IMPORTANT: marginal characteristics grouping indices have to start at 0!
        annual_household_control_totals_data = {
            "year": array(8*[2000]),
            #"age_of_head": array(4*[0] + 4*[1]),
            "age_of_head_min": array([ 0, 0, 0, 0, 50, 50, 50, 50]),
            "age_of_head_max": array([49,49,49,49,100,100,100,100]),
            #"income": array(2*[0] + 2*[1] + 2*[0] + 2*[1]),
            "income_min": array([    0,    0,40000,40000,    0,    0,40000,40000]),
            "income_max": array([39999,39999,   -1,   -1,39999,39999,   -1,   -1]),
            #"persons": array([0,1,0,1,0,1,0,1]),
            "persons_min": array([0, 3,0, 3,0, 3,0, 3]),
            "persons_max": array([2,-1,2,-1,2,-1,2,-1]),
            "total_number_of_households": array([4000, 5000, 1000, 3000, 0, 6000, 3000, 8000])
            }
        ##size of columns was not even, removed last element of min and max
        #household_characteristics_for_ht_data = {
            #"characteristic": array(2*['age_of_head'] + 2*['income'] + 2*['persons']),
            #"min": array([0, 50, 0, 40000, 0, 3]),
            #"max": array([49, 100, 39999, -1, 2, -1]) 
            #}
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=[])

        # unplace some households
        where10 = where(hh_set.get_attribute("grid_id") != 10)[0]
        hh_set.modify_attribute(name="grid_id", data=zeros(where10.size), index=where10)

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        #check that there are indeed 33000 total households after running the model
        results = hh_set.size()
        should_be = [30000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the number of households in each group exactly match the control totals specified
        results = self.get_count_all_groups(hh_set)
        should_be = [4000, 5000, 1000, 3000, 0, 6000, 3000, 8000]
        self.assertEqual(ma.allclose(results, should_be),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def get_count_all_groups(self, hh_set):
        res = zeros(8)
        i=0
        for age_conditional in ["<", ">="]:
            tmp1 = eval("where(hh_set.get_attribute('age_of_head') %s 50, 1,0)" % age_conditional)
            for income_conditional in ["<", ">="]:
                tmp2 = logical_and(tmp1, eval("where(hh_set.get_attribute('income') %s 40000, 1,0)" % income_conditional))
                for persons_conditional in ["<", ">="]:
                    tmp3 = logical_and(tmp2, eval("where(hh_set.get_attribute('persons') %s 3, 1,0)" % persons_conditional))
                    res[i] = tmp3.sum()
                    i+=1
        return res

    def test_controlling_income(self):
        """ Controls for one marginal characteristics, namely income.
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000, 2001, 2001, 2001, 2001, 2002, 2002, 2002, 2002]),
            #"income": array([0,1,2,3,0,1,2,3, 0,1,2,3]),
            "income_min": array([    0,40000, 70000,120000,     0,40000, 70000,120000,     0,40000, 70000,120000]),
            "income_max": array([39999,69999,119999,    -1, 39999,69999,119999,    -1, 39999,69999,119999,    -1]),
            "total_number_of_households": array([25013, 21513, 18227, 18493, # 2000   
                                                 10055, 15003, 17999, 17654, # 2001
                                                 15678, 14001, 20432, 14500]) # 2002
            }

        #household_characteristics_for_ht_data = {
            #"characteristic": array(4*['income']),
            #"min": array([0, 40000, 120000, 70000]), # category 120000 has index 3 and category 70000 has index 2 
            #"max": array([39999, 69999, -1, 119999]) # (testing row invariance)
            #}
        #hc_sorted_index = array([0,1,3,2])
        households_data = {
            "household_id":arange(20000)+1,
            "grid_id": array(19950*[1] + 50*[0]),
            "income": array(1000*[1000] + 1000*[10000] + 2000*[20000] + 1000*[35000] + 2000*[45000] +
                                1000*[50000] + 2000*[67000]+ 2000*[90000] + 1000*[100005] + 2000*[110003] +
                                1000*[120000] + 1000*[200000] + 2000*[500000] + 1000*[630000])
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=[])

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        results = hh_set.size()
        should_be = [83246]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 4
        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[0]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i],
                                     hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[i]).sum()
        results[-1] = (hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+1]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[0:4]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should remove households in all four categories
        model.run(year=2001, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[4:8]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[4]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+4],
                                     hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[i+4]).sum()
        results[-1] = (hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+5]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[4:8]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should add and remove households
        model.run(year=2002, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[8:12]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[8]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+8],
                                     hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[i+8]).sum()
        results[-1] = (hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+9]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[8:12]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def test_controlling_age_of_head(self):
        """ Controls for one marginal characteristics, namely age_of_head.
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2001, 2001, 2001, 2002, 2002, 2002]),
            #"age_of_head": array([0,1,2,0,1,2, 0,1,2]),
            "age_of_head_min": array([ 0,35,65,  0,35,65,  0,35,65]),
            "age_of_head_max": array([34,64,-1, 34,64,-1, 34,64,-1]),
            "total_number_of_households": array([25013, 21513, 18227,  # 2000
                                                 10055, 15003, 17999, # 2001
                                                 15678, 14001, 20432]) # 2002
            }

        #household_characteristics_for_ht_data = {
            #"characteristic": array(3*['age_of_head']),
            #"min": array([0, 35, 65]),
            #"max": array([34, 64, -1])
            #}

        households_data = {
            "household_id":arange(15000)+1,
            "grid_id": array(15000*[1]),
            "age_of_head": array(1000*[25] + 1000*[28] + 2000*[32] + 1000*[34] +
                            2000*[35] + 1000*[40] + 1000*[54]+ 1000*[62] +
                            1000*[65] + 1000*[68] + 2000*[71] + 1000*[98])
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household',
                                      id_name=[])
        
        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[0:3]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[0]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i],
                                     hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[i]).sum()
        results[-1] = (hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+1]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[0:3]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should remove households in all four categories
        model.run(year=2001, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[3:6]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[0]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+3],
                                     hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[i+3]).sum()
        results[-1] = (hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+4]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[3:6]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        model.run(year=2002, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[6:9]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = where(hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[0], 1,0).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+6],
                                     hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[i+6]).sum()
        results[-1] = (hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+7]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[6:9]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        
    def test_controlling_sector(self):
        """ Controls for one marginal characteristics, namely age_of_head.
        """
        annual_employment_control_totals_data = {
            "year": array([2000, 2000, 2000, 2001, 2001, 2001, 2002, 2002, 2002]),
            "sector_id": array([ 1,2,3, 1,2,3,  1,2,3]),
            "number_of_jobs": array([25013, 21513, 18227,  # 2000
                                                 10055, 15003, 17999, # 2001
                                                 15678, 14001, 20432]) # 2002
            }


        jobs_data = {
            "job_id":arange(15000)+1,
            "grid_id": array(15000*[1]),
            "sector_id": array(1000*[1] + 1000*[1] + 2000*[1] + 1000*[1] +
                            2000*[2] + 1000*[2] + 1000*[2]+ 1000*[2] +
                            1000*[3] + 1000*[3] + 2000*[3] + 1000*[3])
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='job_set', table_data=jobs_data)
        job_set = JobDataset(in_storage=storage, in_table_name='job_set')

        storage.write_table(table_name='ect_set', table_data=annual_employment_control_totals_data)
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name='ect_set', what='',
                                      id_name=[])

        
        model = TransitionModel(job_set, control_total_dataset=ect_set)
        model.run(year=2000, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})

        results = job_set.size()
        should_be = [(ect_set.get_attribute("number_of_jobs")[0:3]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = (job_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i]).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[0:3]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        model.run(year=2001, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})
        results = job_set.size()
        should_be = [(ect_set.get_attribute("number_of_jobs")[3:6]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = (job_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i+3]).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[3:6]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        model.run(year=2002, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})
        results = job_set.size()
        should_be = [(ect_set.get_attribute("number_of_jobs")[6:9]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = (job_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i+6]).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[6:9]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def test_accounting_attribute(self):
        """
        """
        annual_employment_control_totals_data = {
            "year":           array([2000,   2000,  2000,  2001]),
            "sector_id":      array([    1,     2,     3,     2]),
            "number_of_jobs": array([25013,  1513,  5000, 10055])
            }


        business_data = {
            "business_id":arange(1500)+1,
            "grid_id": array(1500*[1]),
            "sector_id": array(500*[1] +
                               500*[2] + 
                               500*[3]),
            "jobs":      array(500*[10] + 
                               500*[10] +
                               500*[10]),
                            
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='bs_set', table_data=business_data)
        bs_set = BusinessDataset(in_storage=storage, in_table_name='bs_set')

        storage.write_table(table_name='ect_set', table_data=annual_employment_control_totals_data)
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name='ect_set', what='',
                                      id_name=[])

        model = TransitionModel(bs_set, dataset_accounting_attribute='jobs', control_total_dataset=ect_set)
        model.run(year=2000, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})

        results = bs_set.get_attribute('jobs').sum()
        should_be = [(ect_set.get_attribute("number_of_jobs")[0:3]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=0.1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = ( bs_set.get_attribute('jobs')*(bs_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i])).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[0:3]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
               
    def test_sync_datasets(self):
        annual_household_control_totals_data = {
            "year": array([2000, 2000]),
            "age_of_head_min": array([ 50,  0]),
            "age_of_head_max": array([100, 49]),
            "total_number_of_households": array([25000, 10000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')
        storage.write_table(table_name='persons', table_data=self.persons_data)
        persons = Dataset(in_storage=storage, in_table_name='persons', dataset_name='person', id_name=['person_id'])
        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=[])

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1},
                  sync_dataset=persons, reset_sync_dataset_attribute_value={'job_id':-1})

        self.assertEqual(persons.size(), hh_set['persons'].sum())
        oldest_age = ndimage.maximum(persons['age'], labels=persons['household_id'], index=hh_set['household_id'])
        count_persons = ndimage.sum(ones(persons.size()), labels=persons['household_id'], index=hh_set['household_id'])
        self.assertArraysEqual(hh_set['age_of_head'], asarray(oldest_age))
        self.assertArraysEqual(hh_set['persons'], asarray(count_persons))
        
        self.assertEqual((hh_set['grid_id'] == -1).sum(), 7000, '')
        self.assertTrue((persons['job_id'] == -1).sum() > 7000, '')

    def test_match_exact_target(self):
        """
        """
        annual_employment_control_totals_data = {
            "year":           array([2000,   2000,  2000,  2001]),
            "sector_id":      array([    1,     2,     3,     2]),
            "number_of_jobs": array([25013,  1510,  5000, 10055])
            }


        business_data = {
            "business_id":arange(1500)+1,
            "grid_id": array(1500*[1]),
            "sector_id": array(500*[1] +
                               500*[2] + 
                               500*[3]),
            "jobs":      array(100*[1] + 200*[10] + 200*[25] + 
                               250*[2] + 250*[20] + 
                               250*[2] + 250*[8]),
                            
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='bs_set', table_data=business_data)
        bs_set = BusinessDataset(in_storage=storage, in_table_name='bs_set')

        storage.write_table(table_name='ect_set', table_data=annual_employment_control_totals_data)
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name='ect_set', what='',
                                      id_name=[])

        model = TransitionModel(bs_set, dataset_accounting_attribute='jobs', control_total_dataset=ect_set)
        model.run(year=2000, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})
        results = ndimage.sum(bs_set['jobs'], bs_set['sector_id'], array([1,2,3]))
        results = asarray(results)
        should_be = array([25013,  1510,  5000])
        self.assertArraysEqual(results, should_be)
        
        model.run(year=2001, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})
        results = ndimage.sum(bs_set['jobs'], bs_set['sector_id'], array([1,2,3]))
        results = asarray(results)
        should_be = array([25013,  10055,  5000])
        self.assertTrue(allclose(results, should_be, atol=2))     #difference less than 3 
        self.assertTrue(allclose(results, should_be, rtol=1e-3))  #difference less than 1%
        
if __name__=='__main__':
    opus_unittest.main()
