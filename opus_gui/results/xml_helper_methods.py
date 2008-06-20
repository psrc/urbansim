# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from PyQt4.QtCore import QString, QModelIndex, SIGNAL

def elementsByAttributeValue(domDocument,
                             attribute,
                             value):
    first_child = domDocument.documentElement() 
    matches = []
    _elementsByAttributeValue(first_child = first_child, 
                               domDocument = domDocument, 
                               attribute = QString(attribute), 
                               value = QString(value),
                               matches = matches)

    return matches
       
def _elementsByAttributeValue(first_child,
                              domDocument,
                              attribute,
                              value,
                              matches):

    node = first_child  
    while not node.isNull():
        if node.isElement():
            domElement = node.toElement()
            if domElement.isNull():
                continue

            if domElement.attribute(attribute) == value:
                matches.append((domElement,node))
            
        if node.hasChildNodes():
            first_child = node.firstChild()
            _elementsByAttributeValue(
                   first_child = first_child, 
                   domDocument = domDocument, 
                   attribute = attribute, 
                   value = value, 
                   matches = matches)
        node = node.nextSibling()
            
def get_child_values(parent, child_names):
    child_vals = {}
    node = parent.firstChild()
    while not node.isNull():
        if node.nodeName() in child_names:
            if node.isElement():
                domElement = node.toElement()
                child_vals[str(node.nodeName())] = domElement.text()
        node = node.nextSibling()
    return child_vals

class ResultsManagerXMLHelper:
    
    def __init__(self, toolboxStuff):
        self.toolboxStuff = toolboxStuff
        
    #####################################################
    #########    XML GET CONVENIENCE METHODS     ########
    #####################################################
    
    def get_available_datasets(self):        
        _, available_datasets = self.get_element_attributes(node_name = 'general', 
                                    node_type = None, 
                                    child_attributes = ['available_datasets'])
        available_datasets = available_datasets['available_datasets']
        available_datasets = str(available_datasets)[1:-1].replace("'",'').split(',')
        return available_datasets
        
    def get_available_indicator_names(self, attributes = []):
        return self._get_node_group(node_value = 'indicator', 
                                    node_attribute = 'type', 
                                    child_attributes = attributes)        
    
    def get_available_indicator_group_names(self, attributes = []):
        return self._get_node_group(node_value = 'indicator_group', 
                                    node_attribute = 'type', 
                                    child_attributes = attributes)        
    
    def get_available_run_info(self, attributes = []):
        return self._get_node_group(node_value = 'source_data', 
                                    node_attribute = 'type', 
                                    child_attributes = attributes)        
    
    def get_available_results(self, attributes = []):
        return self._get_node_group(node_value = 'indicator_result', 
                                    node_attribute = 'type', 
                                    child_attributes = attributes)        
    
    def _get_node_group(self,
                        node_value, 
                        node_attribute = 'type',
                        child_attributes = []):
        domDocument = self.toolboxStuff.doc
        node_list = elementsByAttributeValue(
             domDocument = domDocument, 
             attribute = node_attribute, 
             value = node_value)

        group = []
        for element, node in node_list:
            item_name = element.nodeName()
            item_info = {'name' : item_name}

            if child_attributes != []:
                attribute_vals = get_child_values(
                    parent = node,
                    child_names = child_attributes
                )
                item_info.update(attribute_vals) 
            group.append(item_info)

        return group
    
    def get_indicators_in_indicator_group(self, group_name):
        viz_map = {
            'Map (per indicator per year)':'matplotlib_map',
            'Chart (per indicator, spans years)':'matplotlib_chart',
            'Table (per indicator, spans years)':'table_per_attribute',
            'Table (per year, spans indicators)':'table_per_year',
            'ESRI table (for loading in ArcGIS)':'table_esri'
        }
        
        indicator_group_node, _ = self.get_element_attributes(node_name = group_name, 
                                                           node_type = 'indicator_group')
        indicators = {}
        node = indicator_group_node.firstChild()
        while not node.isNull():
            indicator_name = str(node.nodeName())
            vals = get_child_values(
                        parent = node, 
                        child_names = ['visualization_type','dataset_name'])
            visualization_type = viz_map[str(vals['visualization_type'])]
            dataset_name = str(vals['dataset_name'])

            if (visualization_type, dataset_name) not in indicators:
                indicators[(visualization_type, dataset_name)] = [indicator_name]
            else:
                indicators[(visualization_type, dataset_name)].append(indicator_name)
            node = node.nextSibling()
            
        return indicators

    def get_indicator_result_info(self, indicator_name):
        _, info = self.get_element_attributes(
                    node_name = indicator_name, 
                    child_attributes = ['source_data',
                                        'indicator_name',
                                        'dataset_name',
                                        'available_years'], 
                    node_type = 'indicator_result')

        indicator = {}
        indicator['source_data_name'] = str(info['source_data'])
        indicator['indicator_name'] = str(info['indicator_name'])
        indicator['dataset_name'] = str(info['dataset_name'])
        indicator['years'] = [int(y) for y in str(info['available_years']).split(', ')]        
        return indicator
    
    def get_element_attributes(self, node_name, child_attributes = [], node_type = None):
        if not isinstance(node_name, QString):
            node_name = QString(node_name)
        if node_type is not None and not isinstance(node_type, QString):
            node_type = QString(node_type)
        
        domDocument = self.toolboxStuff.doc
        
        elements = domDocument.elementsByTagName(node_name)
        matching_element = None
        
        if node_type is None: 
            if int(elements.length()) > 1:
                raise 'There are multiple xml elements named %s'%str(node_name)
            else: 
                matching_element = elements.item(0)
        else:
            for x in xrange(0,elements.length(),1):
                elementNode = elements.item(x)
                element = elementNode.toElement()
                if not element.isNull():
                    if element.hasAttribute('type') and \
                           (element.attribute('type') == node_type):
                        matching_element = element
                        break

        if not matching_element: 
            raise 'Could not find element %s of type %s'%(str(node_name), str(node_type))

        child_attributes = get_child_values(parent = matching_element, 
                                 child_names = child_attributes)

        return matching_element, child_attributes        
        
    #####################################################
    ##############    XML ADDITIONS    ##############
    #####################################################
                            
    def add_run_to_run_manager_xml(self, cache_directory, 
                                    scenario_name, run_name, 
                                    start_year, end_year):
                
        head_node_args = {'type':'source_data',
                          'value':''}
        
        scenario_def = {
            'name':'scenario_name',
            'type':'string',
            'value':scenario_name,
        }
        run_def = {
            'name':'run_name',
            'type':'string',
            'value':run_name,
        }
        cache_dir_def = {
            'name':'cache_directory',
            'type':'string',
            'value':cache_directory,
        }
        start_year_def = {
            'name':'start_year',
            'type':'integer',
            'value':str(start_year),
        }
        end_year_def = {
            'name':'end_year',
            'type':'integer',
            'value':str(end_year),
        }        
        child_defs = [scenario_def, run_def, cache_dir_def, start_year_def, end_year_def]
        
        name = 'Run_%s'%run_name

        self._add_new_xml_tree(head_node_name = name, 
                               head_node_args = head_node_args, 
                               child_node_definitions = child_defs, 
                               parent_name = 'Simulation_runs',
                               temporary = True,
                               children_hidden = True)

    def add_result_to_xml(self, 
                          result_name,
                          source_data_name,
                          indicator_name,
                          dataset_name,
                          years):
        
        head_node_args = {'type':'indicator_result',
                          'value':''}
        
        source_data_def = {
            'name':'source_data',
            'type':'string',
            'value':source_data_name
        }
        indicator_def = {
            'name':'indicator_name',
            'type':'string',
            'value':indicator_name
        }
        dataset_def = {
            'name':'dataset_name',
            'type':'string',
            'value':dataset_name
        }
        year_def = {
            'name':'available_years',
            'type':'string',
            'value':', '.join([repr(year) for year in years])
        }
        
        child_defs = [source_data_def, indicator_def, dataset_def, year_def]
        
        self._add_new_xml_tree(head_node_name = result_name, 
                               head_node_args = head_node_args, 
                               child_node_definitions = child_defs, 
                               parent_name = 'Results',
                               temporary = True,
                               children_hidden = True)

    def addNewIndicator(self, 
                        indicator_name,
                        package_name,
                        expression):

        head_node_args = {'type':'indicator',
                          'value':''}
        
        package_def = {
            'name':'package',
            'type':'string',
            'value':package_name,
        }
        expression_def = {
            'name':'expression',
            'type':'string',
            'value':expression
        }
        child_defs = [package_def, expression_def]
        
        self._add_new_xml_tree(head_node_name = indicator_name, 
                               head_node_args = head_node_args, 
                               child_node_definitions = child_defs, 
                               parent_name = 'my_indicators',
                               children_hidden = True)
          
    def addNewIndicatorGroup(self, group_name):
        head_node_args = {'type':'indicator_group',
                          'value':''}
                
        self._add_new_xml_tree(head_node_name = group_name, 
                               head_node_args = head_node_args, 
                               parent_name = 'Indicator_groups')

    def addIndicatorToGroup(self, group_name, indicator_name):

        head_node_args = {'type':'indicator_group_member',
                          'value':''}
        
        available_datasets = self.get_available_datasets()        
        datasets = '|'.join(available_datasets)

        visualizations = [
            'Map (per indicator per year)',
            'Chart (per indicator, spans years)',
            'Table (per indicator, spans years)',
            'Table (per year, spans indicators)']
        visualizations = '|'.join(visualizations)
        
        datasets_def = {
            'name':'dataset_name',
            'type':'string',
            'value':'',
            'choices':datasets
        }
        visualization_def = {
            'name':'visualization_type',
            'type':'string',
            'value':'',
            'choices':visualizations
        }
        child_defs = [datasets_def, visualization_def]
        
        self._add_new_xml_tree(head_node_name = indicator_name, 
                               head_node_args = head_node_args, 
                               child_node_definitions = child_defs, 
                               parent_name = group_name)
                
    def _add_new_xml_tree(self, 
                          head_node_name,
                          head_node_args, 
                          parent_name,
                          child_node_definitions = [],
                          temporary = False,
                          children_hidden = False):
        
        model = self.toolboxStuff.resultsManagerTree.model
        document = self.toolboxStuff.doc
        
        
        head_node = model.create_node(document = document, 
                                    name = head_node_name,
                                    temporary = temporary, 
                                    **head_node_args)

            
        parentIndex = model.index(0,0,QModelIndex()).parent()
        current_index = model.findElementIndexByName(parent_name, parentIndex)[0]
        model.insertRow(0,
                current_index,
                head_node)

        if child_node_definitions != []:
            child_nodes = []
            for args in child_node_definitions:
                if children_hidden:
                    if 'flags' in args: 
                        args['flags'] += '|hidden'
                    else:
                        args['flags'] = 'hidden'
                child_node = model.create_node(document = document,
                                               temporary = temporary,
                                               **args)
                child_nodes.append(child_node)
                
            child_index = model.findElementIndexByName(head_node_name, current_index)[0]
            if child_index.isValid():
                for node in sorted(child_nodes, reverse=True):
                    model.insertRow(0,
                                    child_index,
                                    node)
            else:
                print "No valid node was found..."
        model.emit(SIGNAL("layoutChanged()"))
