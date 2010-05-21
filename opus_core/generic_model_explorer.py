# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from numpy import zeros, take, ones
from opus_core.misc import unique_values
from opus_core.datasets.dataset import DatasetSubset
from opus_core.variables.variable_name import VariableName

class GenericModelExplorer(object):
        
    def get_model(self):
        return self.model_system.run_year_namespace["model"]
    
    def get_dataset(self, dataset_name):
        return self.model_system.run_year_namespace["datasets"][dataset_name]
        
    def get_data(self, coefficient, submodel=-2):
        return self.get_model().get_data(coefficient, submodel)

    def get_coefficient_names(self, submodel=-2):
        return self.get_model().get_coefficient_names(submodel)
        
    def get_data_as_dataset(self, submodel=-2):
        return self.get_model().get_data_as_dataset(submodel)
        
    def get_model(self):
        return self.model_system.run_year_namespace["model"]
        
    def get_choice_set(self): # works only for choice models
        return self.get_model().model_interaction.interaction_dataset.get_dataset(2)
    
    def get_choice_set_index(self): # works only for choice models
        return self.get_model().model_interaction.interaction_dataset.get_index(2)
        
    def get_choice_set_index_for_submodel(self, submodel): # works only for choice models
        index = self.get_choice_set_index()
        return take (index, indices=self.get_agent_set_index_for_submodel(submodel), axis=0)
    
    def get_agent_set(self): # works only for choice models
        return self.get_model().model_interaction.interaction_dataset.get_dataset(1)
        
    def get_agent_set_index(self): # works only for choice models
        return self.get_model().model_interaction.interaction_dataset.get_index(1)
        
    def get_agent_set_index_for_submodel(self, submodel):
        model = self.get_model()
        return model.observations_mapping[submodel]
    
    def get_active_agent_set(self):
        """Return agent set that make choices in the model."""
        agents = self.get_agent_set()
        return DatasetSubset(agents, self.get_agent_set_index())
        
    def _get_before_after_dataset_from_attribute(self, var_name):
        dataset_name = var_name.get_dataset_name()
        ds = self.get_dataset(dataset_name)
        ds.copy_attribute_by_reload(var_name)
        return ds
    
    def get_before_after_attribute(self, attribute_name):
        var_name = VariableName(attribute_name)
        ds = self._get_before_after_dataset_from_attribute(var_name)
        return {'after': ds.get_attribute(var_name.get_alias()),
                'before': ds.get_attribute('%s_reload__' % var_name.get_alias())}
        
    def summary_before_after(self, attribute_name):
        var_name = VariableName(attribute_name)
        ds = self._get_before_after_dataset_from_attribute(var_name)
        print ''
        print 'Before model run:'
        print '================='
        ds.summary(names=['%s_reload__' % var_name.get_alias()])
        print ''
        print 'After model run:'
        print '================='
        ds.summary(names=[var_name.get_alias()])
        
    def model_dependencies(self):
        """Prints out variable dependencies for the model."""
        from opus_core.variables.dependency_query import DependencyChart
        model, group = self.get_model_name()
        chart = DependencyChart(self.xml_configuration, model=model, model_group=group, 
                                specification=self.get_specification())
        chart.print_model_dependencies()
        
    def variable_dependencies(self, name):
        """Prints out dependencies of this variable. 'name' can be either an alias from 
        the model specification or an expression."""
        from opus_core.variables.dependency_query import DependencyChart
        varname = None
        allvars = self.get_specification().get_variable_names()
        for ivar in range(len(allvars)):
            if name == allvars[ivar].get_alias():
                varname = allvars[ivar]
                break
        if varname is None:
            varname = VariableName(name)
        chart = DependencyChart(self.xml_configuration)
        chart.print_dependencies(varname.get_expression())
                    
    def plot_histogram_before_after(self, attribute_name, bins=None):
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
        ds = self.get_data_as_dataset(submodel)
        attrs = [attr for attr in ds.get_known_attribute_names() if attr not in ds.get_id_name()]
        return ds.correlation_matrix(attrs)
        
    def get_model_name(self):
        """ Must be defined in a child class. a tuple of model name and model group.
        """
        raise NotImplementedError('get_model_name')
        
    def plot_correlation(self, submodel=-2):
        ds = self.get_data_as_dataset(submodel)
        attrs = [attr for attr in ds.get_known_attribute_names() if attr not in ds.get_id_name()]
        ds.correlation_image(attrs)
        
    def plot_choice_set(self):
        choice_set = self.get_choice_set()
        result = zeros(choice_set.size(), dtype='int16')
        result[unique_values(self.get_choice_set_index().ravel())] = 1
        dummy_attribute_name = '__sampled_choice_set__'
        choice_set.add_attribute(name=dummy_attribute_name, data=result)
        choice_set.plot_map(dummy_attribute_name, background=-1)
        choice_set.delete_one_attribute(dummy_attribute_name)
        
    def plot_choice_set_attribute(self, name):
        choice_set = self.get_choice_set()
        filter_var = ones(choice_set.size(), dtype='int16')
        filter_var[unique_values(self.get_choice_set_index().ravel())] = 0
        dummy_attribute_name = '__sampled_choice_set_filter__'
        choice_set.add_attribute(name=dummy_attribute_name, data=filter_var)
        choice_set.plot_map(name, filter=dummy_attribute_name)
        choice_set.delete_one_attribute(dummy_attribute_name)
        