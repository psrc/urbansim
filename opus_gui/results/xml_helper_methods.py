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
            
def get_child_values(parent, child_names = [], all = False):
    child_vals = {}
    node = parent.firstChild()
    while not node.isNull():
        if all or node.nodeName() in child_names:
            
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
        _, available_datasets_dict = self.get_element_attributes(node_name = 'general', 
                                    node_type = None, 
                                    child_attributes = ['available_datasets'])
        return eval(str(available_datasets_dict['available_datasets']))
    
    def get_available_batches(self, attributes = []):
        return self._get_node_group(node_value = 'indicator_batch', 
                                    node_attribute = 'type', 
                                    child_attributes = attributes)  
                
    def get_available_indicator_names(self, attributes = [],child_attributes = []):
        variables = self._get_node_group(node_value = 'variable_definition', 
                                    node_attribute = 'type', 
                                    child_attributes = child_attributes,
                                    attributes = attributes + ['use', 'source'])   
        indicators = []
        for var in variables:
            if var['use'] != 'model variable' and var['source'] == 'expression':
                indicators.append(var)
        return indicators      
    
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
                        child_attributes = [],
                        attributes = []):
        domDocument = self.toolboxStuff.doc
        node_list = elementsByAttributeValue(
             domDocument = domDocument, 
             attribute = node_attribute, 
             value = node_value)

        group = []
        for element, node in node_list:
            item_name = element.nodeName()
            item_info = {'name' : item_name,
                         'value': element.text()}
            
            for attribute in attributes:
                item_info[attribute] = element.attribute(QString(attribute))

            if child_attributes != []:
                attribute_vals = get_child_values(
                    parent = node,
                    child_names = child_attributes
                )
                item_info.update(attribute_vals) 
            group.append(item_info)

        return group
    
    def get_visualization_options(self):
        viz_map = {
#            'Map (per indicator per year)':'matplotlib_map',
#            'Chart (per indicator, spans years)':'matplotlib_chart',
#            'Table (per indicator, spans years)':'table_per_attribute',
            'Table (per year, spans indicators)':'table_per_year',
#            'ESRI table (for loading in ArcGIS)':'table_esri'
        }
        return viz_map
        
    def get_batch_configuration(self, batch_name):
        visualizations = []
        
        batch_node, _ = self.get_element_attributes(node_name = batch_name, 
                                                    node_type = 'indicator_batch')
        
        node = batch_node.firstChild()
        while not node.isNull():
            element = node.toElement()
            vals = get_child_values(parent = element,
                                    all = True)
            
            visualization_type = str(vals['visualization_type'])
            dataset_name = str(vals['dataset_name'])
            vals['name'] = str(node.nodeName())
            visualizations.append((visualization_type, dataset_name, vals))
            
            node = node.nextSibling()
            
        return visualizations 



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
    
    def get_element_attributes(self, node_name, child_attributes = [], all = False, node_type = None):
        if not isinstance(node_name, QString):
            node_name = QString(node_name)
        if node_type is not None and not isinstance(node_type, QString):
            node_type = QString(node_type)
        
        domDocument = self.toolboxStuff.doc
        
        elements = domDocument.elementsByTagName(node_name)
        matching_element = None
        
        if node_type is None: 
            if int(elements.length()) > 1:
                raise Exception('There are multiple xml elements named %s'%str(node_name))
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
            raise Exception('Could not find element %s of type %s'%(str(node_name), str(node_type)))

        child_attributes = get_child_values(parent = matching_element, 
                                 child_names = child_attributes,
                                 all = all)
        return matching_element, child_attributes        
        
        
    #####################################################
    ##############    XML REMOVAL    ####################
    #####################################################
    
    #####################################################
    #####################################################
    ##############    XML ADDITIONS    ##############
    #####################################################
                            
    def add_run_to_run_manager_xml(self, cache_directory, 
                                    scenario_name, run_name, 
                                    start_year, end_year,
                                    temporary = False):
                
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
        
        self._add_new_xml_tree(head_node_name = run_name, 
                               head_node_args = head_node_args, 
                               child_node_definitions = child_defs, 
                               parent_name = 'Simulation_runs',
                               temporary = temporary,
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
          
    def addNewIndicatorBatch(self, batch_name):
        head_node_args = {'type':'indicator_batch',
                          'value':''}
                
        self._add_new_xml_tree(head_node_name = batch_name, 
                               head_node_args = head_node_args, 
                               parent_name = 'Indicator_batches')

    def addNewVisualizationToBatch(self, viz_name, batch_name, viz_type, viz_params):
        head_node_args = {'type':'batch_visualization',
                          'value':''}

        viz_params.append({'value':self.get_visualization_options()[viz_type],
                           'name':'visualization_type'})
            
        for param in viz_params:
            value = param['value']
            if isinstance(value,str) or isinstance(value,QString):
                param['type'] = 'string'
                param['value'] = value
            elif isinstance(value,list):
                param['type'] = 'list'
            elif isinstance(value,int):
                param['type'] = 'integer'
        
        self._add_new_xml_tree(head_node_name = QString(viz_name), 
                               head_node_args = head_node_args, 
                               parent_name = batch_name, 
                               child_node_definitions = viz_params, 
                               temporary = False, 
                               children_hidden = True)
                
    def _insert_children(self, head_node, child_node_definitions, children_hidden = True, temporary = False):
        # Loop through all the child definitions and create nodes if they are needed
        if child_node_definitions == []: return

        # This list is to hold all of the child dom nodes created
        model = self.toolboxStuff.resultsManagerTree.model

        child_nodes = []
        for args in child_node_definitions:
            if children_hidden:
                if 'flags' in args: 
                    args['flags'] += '|hidden'
                else:
                    args['flags'] = 'hidden'
            child_node = model.create_node(document = self.toolboxStuff.doc,
                                           temporary = temporary,
                                           **args)
            child_nodes.append(child_node)
        # Now loop through the nodes we created to append them to the head_node
        for node in sorted(child_nodes, reverse=True):
            head_node.appendChild(node)
                
                
    def _add_new_xml_tree(self, 
                          head_node_name,
                          head_node_args, 
                          parent_name,
                          child_node_definitions = [],
                          temporary = False,
                          children_hidden = False):
        
        model = self.toolboxStuff.resultsManagerTree.model
        document = self.toolboxStuff.doc
        
        # The new head node to add children to and then insert
        head_node = model.create_node(document = document, 
                                    name = head_node_name,
                                    temporary = temporary, 
                                    **head_node_args)

        self._insert_children(head_node=head_node, 
                              child_node_definitions=child_node_definitions, 
                              children_hidden=children_hidden, 
                              temporary=temporary)

        # Find the parent node index to append to
        parentIndex = model.index(0,0,QModelIndex()).parent()
        current_index = model.findElementIndexByName(parent_name, parentIndex)[0]

        # Now insert the head_node
        model.insertRow(0,
                        current_index,
                        head_node)

        model.emit(SIGNAL("layoutChanged()"))
        
    def update_dom_node(self, index, new_base_node_name = None, children_to_update = None, children_hidden = True, temporary = False):
        if index is None: return 
        
        model = self.toolboxStuff.resultsManagerTree.model
        # Keep track of any edits so we can mark the GUI as edited and force a save
        # as well as make the node editable if it is not already...
        dirty = False
        # Grab the base node... this is a QDomNode
        base_node = index.internalPointer().node()

        if not base_node.isNull() and new_base_node_name is not None:
            # We only want to check out this node if it is of type "element"
            if base_node.isElement():
                domElement = base_node.toElement()
                if not domElement.isNull():
                    # Now we check to see if the tagname is the one we are looking for
                    name = str(domElement.tagName())
                    # and more importantly if it has changed... we only update on a changed value
                    if name != new_base_node_name:
                        # This path is to allow us to verify if the node being modified
                        # is inherited and needs to be added back in
                        domNodePath = model.domNodePath(base_node)
                        # Actually update the tagname
                        domElement.setTagName(QString(new_base_node_name))
                        # Now search and check if inherited and needs to be added back in to tree
                        model.checkIfInheritedAndAddBackToTree(domNodePath, index.parent())
                        # We have made updates so we need to do the "dirty stuff" later
                        dirty = True

        # Lets avoid calling setData directly... Will create a new method that will do the above
        #self.model.setData(self.selected_index,QVariant(indicator_name),Qt.EditRole)
        
        # Get the first child node (also a QDomNode) for traversal
        node = base_node.firstChild()
        
        # Only march on if we have non-null nodes
        while not node.isNull():
            # We only want to check out this node if it is of type "element"
            if node.isElement():
                domElement = node.toElement()
                if not domElement.isNull():
                    # Now we check to see if the tagname is the one we are looking for
                    name = str(domElement.tagName())
                    if name in children_to_update:
                        # We have a match se we need to grab the text node for the element
                        elementText = str(domElement.text())
                        # If the text node value has changed we need to update
                        if elementText != children_to_update[name]:
                            # We need to grab the text node from the element
                            if domElement.hasChildNodes():
                                children = domElement.childNodes()
                                for x in xrange(0,children.count(),1):
                                    if children.item(x).isText():
                                        textNode = children.item(x).toText()
                                        # Finally set the text node value
                                        textNode.setData(children_to_update[name])

                                        # We have made this element dirty so we need to mark it all dirty
                                        dirty = True
                        del children_to_update[name]
            # Continue to loop through children
            node = node.nextSibling()
        
        #add children which did not already exist
        self._insert_children(head_node=base_node, 
                              child_node_definitions=self._convert_to_node_dictionary(child_dictionary = children_to_update), 
                              children_hidden = children_hidden, 
                              temporary=temporary)
                    
        # TODO: Should gather all of this into a method in the model to allow for bulk update
        if dirty:    
            # If we have changed something we need to make sure the node we are editing is marked
            # as editable since there was no check that the node was editable before allowing
            # the right click edit option.
            model.makeEditable(base_node)
            # Flag the model as dirty to prompt for save
            model.markAsDirty()
        
    def _convert_to_node_dictionary(self, child_dictionary):
        type_map = {
            str:'string',
            list:'list',
            int:'integer',
            QString:'string'
        }
        node_vals = []
        for k,v in child_dictionary.items():
            node_vals.append({'name':k, 'value':v, 'type':type_map[type(v)]})
            
        return node_vals
        
        
        
        
