# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.general_manager.controllers.xml_configuration.xml_controller_general import XmlController_General

'''
Methods and Classes related to the General Manager
'''

def get_available_dataset_names(project):
    '''
    Get a list of the dataset names that are available in the project.
    @param project (OpusProject): project to extract datasets from
    @return: list of dataset names (list(String))
    '''
    return _get_list(project = project,
                     xpath = 'general/available_datasets')

def get_available_spatial_dataset_names(project):
    '''
    Get a list of the spatial dataset names that are available in the project.
    @param project (OpusProject): project to extract datasets from
    @return: list of dataset names (list(String))
    '''
    return _get_list(project = project,
                     xpath = 'general/spatial_datasets')

def _get_list(project, xpath):
    if project is None:
        return []
    list_node = project.find(xpath)
    list_text = list_node.text
    # turn the Python syntax list into a clean, comma separated, list
    for char in '[]\'"':
        list_text = list_text.replace(char, '')
    return [element.strip() for element in
           list_text.split(',')] 
    
def get_variable_nodes_per_dataset(project):
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
    for variable_node in expression_library_node:
        if not variable_node.get('type') == 'variable_definition':
            continue # Skip non-variables
        dataset_name = variable_node.get('dataset')
        if not dataset_name in var_nodes_per_dataset:
            var_nodes_per_dataset[dataset_name] = []
        var_nodes_per_dataset[dataset_name].append(variable_node)
    return var_nodes_per_dataset

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
        indicators_per_dataset[dataset] = [node for node in variables if node.get('use') in ('both', 'indicator')]
        
    return indicators_per_dataset

def get_available_indicator_nodes(project):
    '''
    Get node objects for all the indicator variables in the project.
    @param project (OpusProject): project to extract variables from
    @return all variables used as indicators (list(Element))
    '''
    variable_nodes_per_dataset = get_variable_nodes_per_dataset(project)
    indicator_nodes = []
    for variable_nodes in variable_nodes_per_dataset.values():
        indicator_nodes.extend([node for node in variable_nodes if
                                node.get('use') in ('both', 'indicator')])
    return indicator_nodes

def get_available_indicator_names(project):
    ''' Get just the names of indicator nodes (list(String)) '''
    return [node.tag for node in get_available_indicator_nodes(project)]


class GeneralManager(AbstractManager):

    ''' Handler for GUI elements belonging to the Generals tab '''

    def __init__(self, base_widget, tab_widget, project):
        AbstractManager.__init__(self, base_widget, tab_widget,
                                 project, 'general')
        self.xml_controller = XmlController_General(self)
