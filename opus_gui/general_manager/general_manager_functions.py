# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
from opus_core.configurations.xml_configuration import get_variable_dataset
from lxml import etree

'''
Methods and Classes related to the General Manager
'''

def get_available_dataset_names(project):
    '''
    Get a list of the dataset names that are available in the project.
    @param project (OpusProject): project to extract datasets from
    @return: list of dataset names (list(String))
    '''
    return _convert_list_from_node(project = project, xpath = 'general/available_datasets')

def get_available_spatial_dataset_names(project):
    '''
    Get a list of the spatial dataset names that are available in the project.
    @param project (OpusProject): project to extract datasets from
    @return: list of dataset names (list(String))
    '''
    return _convert_list_from_node(project = project, xpath = 'general/spatial_datasets')

def _convert_list_from_node(project, xpath):
    if project is None:
        return []
    list_node = project.find(xpath)
    list_text = list_node.text
    # turn the Python syntax list into a comma separated list
    for char in '[]\'"':
        list_text = list_text.replace(char, '')
    return [element.strip() for element in list_text.split(',')]

def get_variable_nodes_per_dataset(project, skip_builtin = False):
    '''
    Get all XML nodes for variables arranged as a dict based on their dataset.
    @param project (OpusProject): project to extract variables from
    @return mapping of datasets and variable nodes
        dict(dataset (String), variable nodes (list(Element))
    '''
    if project is None:
        return {}
    expression_library_node = project.find('general/expression_library')
    if expression_library_node is None:
        return {}

    var_nodes_per_dataset = {}
    for variable_node in expression_library_node.findall('variable'):
        dataset_name = get_variable_dataset(variable_node)
        if dataset_name == '':
            if skip_builtin:
                continue
            else:
                dataset_name = '<built-in>'
        if not dataset_name in var_nodes_per_dataset:
            var_nodes_per_dataset[dataset_name] = []
        var_nodes_per_dataset[dataset_name].append(variable_node)
    return var_nodes_per_dataset

def get_built_in_variable_nodes():
    '''
    Get a list of all built in variables in the project. These are variables that are not connected
    to any particular dataset.
    The list of built in variables is hard coded at this point, but may change in the future.
    '''
    constant_node = etree.Element('variable', {'type': 'variable_definition', 'name': 'constant'})
    return [constant_node,]

def get_indicator_nodes_per_dataset(project):
    '''
    Get all XML nodes for variables arranged as a dict based on their dataset.
    @param project (OpusProject): project to extract variables from
    @return mapping of datasets and variable nodes
        dict(dataset (String), variable nodes (list(Element))
    '''
    variable_nodes_per_dataset = get_variable_nodes_per_dataset(project)
    indicators_per_dataset = {}
    for dataset, variables in variable_nodes_per_dataset.items():
        indicators_per_dataset[dataset] = [node for node in variables if
                                           node.get('use') in ('both', 'indicator')]
    return indicators_per_dataset

def get_available_indicator_nodes(project):
    '''
    Get node objects for all the indicator variables in the project.
    @param project (OpusProject): project to extract variables from
    @return all variables used as indicators (list(Element))
    '''
    all_indicator_nodes = []
    indicator_nodes_per_dataset = get_indicator_nodes_per_dataset(project)
    # flatten dict
    map(all_indicator_nodes.extend, indicator_nodes_per_dataset.values())
    return all_indicator_nodes

def get_available_indicator_names(project):
    ''' Get just the names of indicator nodes (list(String)) '''
    return [node.get('name') for node in get_available_indicator_nodes(project)]

