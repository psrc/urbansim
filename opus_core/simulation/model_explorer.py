# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from opus_core.configuration import Configuration
from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.utils.cache_flt_data import CacheFltData
from opus_core.model_coordinators.model_system import ModelSystem
from opus_core.choice_model import ChoiceModel
from numpy import zeros, take, ones, where, reshape, concatenate, array
from opus_core.misc import unique, write_table_to_text_file, write_to_text_file
from opus_core.datasets.dataset import DatasetSubset
from opus_core.variables.variable_name import VariableName
from opus_core.specified_coefficients import SpecifiedCoefficientsFor1Submodel
from opus_core.plot_functions import plot_barchart

class ModelExplorer(object):
    def __init__(self, model, year, scenario_name=None, model_group=None, configuration=None, xml_configuration=None, 
                 cache_directory=None):
        self.model_group = model_group
        self.explored_model = model
 
        if configuration is None:
            if xml_configuration is None:
                raise StandardError, "Either dictionary based or XML based configuration must be given."
            config = xml_configuration.get_run_configuration(scenario_name)
        else:
            config = Configuration(configuration)
            
        self.scenario_models = config['models']
        if config.get('models_in_year', None) is not None and config['models_in_year'].get(year, None) is not None:
            del config['models_in_year'][year]
        if model is not None:
            dependent_models = config['models_configuration'][model]['controller'].get('dependencies', [])
            config['models'] = dependent_models
            if model_group is None:
                config['models'] = config['models'] + [{model: ["run"]}]
            else:
                config['models'] = config['models'] + [{model: {"group_members": [{model_group: ["run"]}]}}]
        else:
            config['models'] = []
            
        config['years'] = [year, year]
        config["datasets_to_cache_after_each_model"]=[]
        config['flush_variables'] = False
        
        self.config = Resources(config)
        self.xml_configuration = xml_configuration
        
        if cache_directory is None:
            cache_directory = config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy
        self.simulation_state = SimulationState(new_instance=True, base_cache_dir=cache_directory, 
                                                start_time=config.get('base_year', 0))
        self.config['cache_directory'] = cache_directory
        
        SessionConfiguration(new_instance=True,
                             package_order=self.config['dataset_pool_configuration'].package_order,
                             in_storage=AttributeCache())
        
    def run(self):
        self.model_system = ModelSystem()
        self.model_system.run(self.config, write_datasets_to_cache_at_end_of_year=False,
                              cleanup_datasets=False)
        logger.log_status("Data cache in %s" % self.simulation_state.get_cache_directory())
        
    def get_agents_for_simulation(self):
        return self.get_active_agent_set()
        
    def get_model_name(self):
        return (self.explored_model, self.model_group)
        
    def get_specification(self):
        return self.get_model().get_specified_coefficients().specification
    
    def get_probabilities(self, submodel=-2):
        """Return a tuple of probabilities and choices, see ChoiceModel.get_probabilities_and_choices.
        Works only for the ChoiceModel class.
        """
        model = self.get_model()
        #if isinstance(model, ChoiceModel):
        return model.get_probabilities_and_choices(submodel)
        #print '\nMethod is implemented only for ChoiceModels.\n'

    def export_probabilities(self, submodel=-2, filename='./choice_model.txt'):
        """Export probabilities and choices into a file. Works only for the ChoiceModel class"""
        
        model = self.get_model()
        #if isinstance(model, ChoiceModel):
        model.export_probabilities(submodel, file_name=filename)
        #else:
        #    print '\nMethod is implemented only for ChoiceModels.\n'
            
    def get_model(self):
        """Return a model object."""
        return self.model_system.run_year_namespace["model"]
    
    def get_dataset(self, dataset_name):
        """Return a Dataset object of the given name."""
        ds = self.model_system.run_year_namespace.get(dataset_name, None)
        if ds is None:
            if dataset_name not in self.model_system.run_year_namespace["datasets"].keys():
                ds = self.get_dataset_pool().get_dataset(dataset_name)
            else:
                ds = self.model_system.run_year_namespace["datasets"][dataset_name]
        return ds
        
    def get_data(self, coefficient, submodel=-2):
        """Calls method get_data of the Model object. Should return a data array for the 
        given coefficient and submodel. Can be used only on in models that are estimable."""
        return self.get_model().get_data(coefficient, submodel)

    def get_coefficient_names(self, submodel=-2):
        """Calls method get_coefficient_names of the Model object which should return
           coefficient names for the given submodel. Can be used only on in models that are estimable."""
        return self.get_model().get_coefficient_names(submodel)
    
    def get_coefficients(self, submodel=-2):
        """Return an object of class SpecifiedCoefficientsFor1Submodel giving the model coefficients. 
        Can be used only on in models that are estimable."""
        return SpecifiedCoefficientsFor1Submodel(self.get_model().get_specified_coefficients(), submodel)

    def get_data_as_dataset(self, submodel=-2, **kwargs):
        """Calls method get_data_as_dataset of the Model object which should return
        an object of class Dataset containing model data. 
        Works only for ChoiceModel (returns InteractionDataset), 
        and for RegressionModel (returns Dataset). 
        """
        return self.get_model().get_data_as_dataset(submodel, **kwargs)
                
    def get_choice_set(self): 
        """Return a Dataset of choices. Works only for the ChoiceModel class.
        """
        return self.get_model().model_interaction.interaction_dataset.get_dataset(2)
    
    def get_choice_set_index(self):
        """Return an array of indices of choices. Works only for the ChoiceModel class.
        """
        return self.get_model().model_interaction.interaction_dataset.get_index(2)
        
    def get_choice_set_index_for_submodel(self, submodel):
        """Return an array of indices of choices for the given submodel. 
        Works only for the ChoiceModel class.
        """
        index = self.get_choice_set_index()
        return take (index, indices=self.get_model().observations_mapping[submodel], axis=0)
    
    def get_active_choice_set(self, submodel=None):
        """Return choice set as seen by agents in the model.
        Works only for the ChoiceModel class.
        """
        if submodel is None:
            choices = self.get_choice_set_index()
        else:
            choices = self.get_choice_set_index_for_submodel(submodel)
        choices = unique(choices.flatten())
        ds = self.get_choice_set()
        return DatasetSubset(ds, choices)
                             
    def get_agent_set(self):
        """Return a Dataset of all agents. Works only for the ChoiceModel class.
        """
        return self.get_model().model_interaction.interaction_dataset.get_dataset(1)
        
    def get_agent_set_index(self):
        """Return an array of indices of agents that are the choosers. 
        Works only for the ChoiceModel class.
        """
        return self.get_model().model_interaction.interaction_dataset.get_index(1)
        
    def get_agent_set_index_for_submodel(self, submodel):
        """Return an array of indices of agents for the given submodel that are the choosers. 
        Works only for the ChoiceModel class.
        """
        model = self.get_model()
        return model.model_interaction.interaction_dataset.get_index(1)[model.observations_mapping[submodel]]
    
    def get_active_agent_set(self, submodel=None):
        """Return agent set that make choices in the model.
        Works only for the ChoiceModel class.
        """
        agents = self.get_agent_set()
        if submodel is None:
            index = self.get_agent_set_index()
        else:
            index = self.get_agent_set_index_for_submodel(submodel)
        return DatasetSubset(agents, index)
    
    def agent_summary(self, submodel=None):
        ds = self.get_active_agent_set(submodel=submodel)
        ds.summary()
        
    def choice_summary(self, submodel=None):
        ds = self.get_active_choice_set(submodel=submodel)
        ds.summary()
       
    def data_summary(self, **kwargs):
        ds = self.get_data_as_dataset(**kwargs)
        ds.summary()
        
    def _get_before_after_dataset_from_attribute(self, var_name, storage, **kwargs):
        dataset_name = var_name.get_dataset_name()
        ds = self.get_dataset(dataset_name)
        ds.compute_variables([var_name], dataset_pool=self.get_dataset_pool())
        ds.copy_attribute_by_reload(var_name, storage=storage, **kwargs)
        return ds
    
    def get_before_after_attribute(self, attribute_name):
        """Return a dictionary with elements 'before' (contains an array of the given attribute
        that is reloaded from the cache) and 'after' (contains an array of the given attribute 
        with the current values).
        """
        from opus_core.store.attribute_cache import AttributeCache
        var_name = VariableName(attribute_name)
        storage = AttributeCache(self.simulation_state.get_cache_directory())
        ds = self._get_before_after_dataset_from_attribute(var_name, storage=storage,
                   package_order=self.get_dataset_pool().get_package_order())       
        return {'after': ds[var_name.get_alias()],
                'before': ds.get_attribute('%s_reload__' % var_name.get_alias())}
        
    def summary_before_after(self, attribute_name):
        """Print summary of the given attribute 'before' (values
        reloaded from the cache) and 'after' (current values).
        """
        from opus_core.store.attribute_cache import AttributeCache
        var_name = VariableName(attribute_name)
        storage = AttributeCache(self.simulation_state.get_cache_directory())
        ds = self._get_before_after_dataset_from_attribute(var_name, storage=storage, 
                   package_order=self.get_dataset_pool().get_package_order())
        print ''
        print 'Before model run:'
        print '================='
        ds.summary(names=['%s_reload__' % var_name.get_alias()])
        print ''
        print 'After model run:'
        print '================='
        #ds.summary(names=[var_name.get_alias()])
        ds.summary(names=[var_name.get_alias()])
        
    def model_dependencies(self, model=None, group=None):
        """Prints out all dependencies for the model."""
        from opus_core.variables.dependency_query import DependencyChart
        if model is None: # current model
            model, group = self.get_model_name()
            spec = self.get_specification()
        else:
            spec = None
        if model == 'all': # print dependencies for all models
            for thismodel in self.scenario_models:
                thisgroups = None
                if isinstance(thismodel, dict):
                    thisgroups = thismodel[thismodel.keys()[0]].get('group_members', None)
                    thismodel = thismodel.keys()[0]
                if not isinstance(thisgroups, list):
                    thisgroups = [thisgroups]                
                for group in thisgroups:
                    chart = DependencyChart(self.xml_configuration, model=thismodel, model_group=group)
                    chart.print_model_dependencies()
        else:
            chart = DependencyChart(self.xml_configuration, model=model, model_group=group, 
                                specification=spec)
            chart.print_model_dependencies()
        
    def variable_dependencies(self, name):
        """Prints out dependencies of this variable. 'name' can be either an alias from 
        the model specification or an expression."""
        from opus_core.variables.dependency_query import DependencyChart
        varname = None
        allvars = self.get_specification().get_variable_names()
        for ivar in range(len(allvars)):
            thisvar = allvars[ivar]
            if not isinstance(thisvar, VariableName):
                thisvar = VariableName(thisvar)
            if name == thisvar.get_alias():
                varname = thisvar
                break
        if varname is None:
            varname = VariableName(name)
        chart = DependencyChart(self.xml_configuration)
        chart.print_dependencies(varname.get_expression())
              
    def compute_expression(self, attribute_name):
        """Compute any expression and return its values."""
        var_name = VariableName(attribute_name)
        dataset_name = var_name.get_dataset_name()
        ds = self.get_dataset(dataset_name)
        return ds.compute_variables([var_name], dataset_pool=self.get_dataset_pool())
        
    def get_dataset_pool(self):
        return self.model_system.run_year_namespace["dataset_pool"]
    
    def plot_histogram_before_after(self, attribute_name, bins=None):
        """Plot histograms of values returned by the method get_before_after_attribute."""
        from opus_core.plot_functions import create_histogram, show_plots
        from matplotlib.pylab import figure
        values = self.get_before_after_attribute(attribute_name)
        alias = VariableName(attribute_name).get_alias()
        fig = figure()
        fig.add_subplot(121)
        create_histogram(values['before'], main='%s (before)' % alias, bins=bins)
        fig.add_subplot(122)
        create_histogram(values['after'], main='%s (after)' % alias, bins=bins)
        show_plots()
        
    def get_correlation(self, submodel=-2):
        """Return an array of correlations between all variables of the model data (for given submodel).
        Works only for ChoiceModel and RegressionModel"""
        ds = self.get_data_as_dataset(submodel)
        attrs = [attr for attr in ds.get_known_attribute_names() if attr not in ds.get_id_name()]
        return ds.correlation_matrix(attrs)
        
    def plot_correlation(self, submodel=-2, useR=False, **kwargs):
        """Plot correlations between all variables of the model data (for given submodel).
        Works only for ChoiceModel and RegressionModel"""
        ds = self.get_data_as_dataset(submodel)
        attrs = [attr for attr in ds.get_known_attribute_names() if attr not in ds.get_id_name()]
        ds.correlation_image(attrs, useR=useR, **kwargs)
        
    def plot_choice_set(self, agents_index=None, aggregate_to=None, matplotlib=True, **kwargs):
        """Plot map of the sampled choice set. 
        agents_index can be given to restrict the set of agents to which the choice set belongs to. 
        aggregate_to is a name of a dataset which the choice set should be aggregated to.
        If matplotlib is False, mapnik is used (and required). 
        Additional arguments are passed to plot_map or plot_map_matplotlib.
        E.g. (choice set are buildings, aggregated to zones, for the first agent)
        er.plot_choice_set(aggregate_to='zone', matplotlib=False, project_name='psrc_parcel', 
                            file='choice_set0.png', agents_index=0)
        """
        choice_set = self.get_choice_set()
        if agents_index is None:
            flatten_choice_index = self.get_choice_set_index().ravel()
        else:
            flatten_choice_index = self.get_choice_set_index()[agents_index,:].ravel()
        if aggregate_to is not None:
            ds_aggr = self.get_dataset(aggregate_to)
            result = ds_aggr.sum_over_ids(choice_set[ds_aggr.get_id_name()[0]][flatten_choice_index], 
                                               ones(flatten_choice_index.size))
            ds = ds_aggr
        else:
            result = choice_set.sum_over_ids(choice_set.get_id_attribute()[flatten_choice_index], 
                                             ones(flatten_choice_index.size))
            ds = choice_set
        dummy_attribute_name = '__sampled_choice_set__'
        ds.add_attribute(name=dummy_attribute_name, data=result)
        if matplotlib:
            coord_syst = None
            if ds.get_coordinate_system() is None and hasattr(ds, 'compute_coordinate_system'):
                coord_syst = ds.compute_coordinate_system(dataset_pool=self.get_dataset_pool())
            ds.plot_map_matplotlib(dummy_attribute_name, background=-1, coordinate_system=coord_syst, **kwargs)
        else:
            ds.plot_map(dummy_attribute_name, background=-1, **kwargs)
        ds.delete_one_attribute(dummy_attribute_name)
        
    def plot_choice_set_attribute(self, name, agents_index=None, aggregate_to=None, function='sum', 
                                  matplotlib=True, **kwargs):
        """Plot map of the given attribute for the sampled choice set.
        agents_index can be given to restrict the set of agents to which the choice set belongs to. 
        aggregate_to is a name of a dataset which the choice set should be aggregated to.
        function defines the aggregating function (e.g. sum, mean, median, etc.)
        If matplotlib is False, mapnik is used (and required). 
        Additional arguments are passed to plot_map or plot_map_matplotlib.
        E.g. er.plot_choice_set_attribute('residential_units', aggregate_to='zone', matplotlib=False, 
                                    project_name='psrc_parcel', file='choice_resunits.png')
        """
        choice_set = self.get_choice_set()
        if agents_index is None:
            flatten_choice_index = self.get_choice_set_index().ravel()
        else:
            flatten_choice_index = self.get_choice_set_index()[agents_index,:].ravel()
        filter_var = ones(choice_set.size(), dtype='int16')
        filter_var[unique(flatten_choice_index)] = 0
        filter_idx = where(filter_var)[0]
        if aggregate_to is not None:
            ds_aggr = self.get_dataset(aggregate_to)
            result = ds_aggr.aggregate_over_ids(choice_set[ds_aggr.get_id_name()[0]][flatten_choice_index], 
                                                     what=choice_set[name][flatten_choice_index], function=function)
            filter = ds_aggr.sum_over_ids(choice_set[ds_aggr.get_id_name()[0]][filter_idx], 
                                                     ones(filter_idx.size))
            filter = filter > 0
            ds = ds_aggr
        else:
            result = choice_set.aggregate_over_ids(choice_set.get_id_attribute()[flatten_choice_index], 
                                                   what=choice_set[name][flatten_choice_index], function=function)
            filter = filter_var
            ds = choice_set
        dummy_attribute_name = '__sampled_choice_set_attribute__'
        ds.add_attribute(name=dummy_attribute_name, data=result)
        dummy_filter_name = '__sampled_choice_set_filter__'
        ds.add_attribute(name=dummy_filter_name, data=filter)
        if matplotlib:
            coord_syst = None
            if ds.get_coordinate_system() is None and hasattr(ds, 'compute_coordinate_system'):
                coord_syst = ds.compute_coordinate_system(dataset_pool=self.get_dataset_pool())
            ds.plot_map_matplotlib(dummy_attribute_name, filter=dummy_filter_name, coordinate_system=coord_syst, **kwargs)
        else:
            ds.plot_map(dummy_attribute_name, filter=dummy_filter_name, **kwargs)
        ds.delete_one_attribute(dummy_attribute_name)
        ds.delete_one_attribute(dummy_filter_name)
                   
    def plot_coefficients(self, submodel=-2, exclude_constant=True, eqidx=0, plot=True, 
                          store_values_to_file=None):
        """ Plot a barchart of coefficient values. This can be used in a regression model, 
        when coefficients are standardized 
        (i.e. using the estimation module opus_core.estimate_linear_regression_standardized).
        store_values_to_file can be a file name where the values are stored.
        """
        coef = self.get_coefficients(submodel)
        values = coef.get_coefficient_values()
        names = coef.get_coefficient_names()
        sd = coef.get_standard_errors()
        idx=ones(names.shape[1], dtype="bool")
        if exclude_constant:
            pos = coef.get_constants_positions()
            if pos.size > 0:               
                idx[pos]=0
        if store_values_to_file is not None:
            n = idx.sum()
            result = concatenate((reshape(names[eqidx, idx], (n,1)), 
                                 reshape(values[eqidx, idx], (n,1)),
                                 reshape(sd[eqidx, idx], (n,1))), axis=1)
            write_to_text_file(store_values_to_file, array(['coefficient_name', 'estimate', 'standard_error']), 
                               delimiter='\t')
            write_table_to_text_file(store_values_to_file, result, delimiter='\t', mode='a')
        if plot:
            plot_barchart(values[eqidx, idx], labels = names[eqidx, idx], errors=sd[eqidx, idx])
        else:
            return {'names': names[eqidx, idx], 'values': values[eqidx, idx], 'errors': sd[eqidx, idx]}
        
    def create_latex_tables(self, directory, other_info_keys=None):
        from opus_core.latex_table_creator import LatexTableCreator
        LTC = LatexTableCreator()
        LTC.create_latex_table_for_coefficients_for_model(
            self.get_model().get_specified_coefficients().coefficients, self.explored_model, directory, 
                                other_info_keys=other_info_keys)
        LTC.create_latex_table_for_specifications_for_model(
            self.get_model().get_specified_coefficients().specification, self.explored_model, directory)

        
