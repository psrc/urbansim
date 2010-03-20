# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml.etree import SubElement

from opus_core.configurations.xml_configuration import node_identity_string, element_id

def _create_or_get_parent(nodes_to_parent, new_project):
    '''helper method to create a node path in the new project like the one of the templated node'''
    if nodes_to_parent == []: # reached the project root
        return new_project.root_node()
    
    # check if the new project contains a node at the current position
    current_node_id_string = node_identity_string(nodes_to_parent[0])
    current_node = new_project.find_by_id_string(current_node_id_string) 
    if current_node is not None:
        return current_node # this was an existing node so we can build down from here
    
    # the current_node doesn't existing in the new project. Extract the missing node's tag and name from the 
    # templated node, get the (created or existing) parent node, and create the current node with the missing
    # tag and name
    missing_node = nodes_to_parent.pop(0) # consume the closest node
    missing_node_tag, missing_node_name = missing_node.tag, missing_node.get('name', None)
    parent_node = _create_or_get_parent(nodes_to_parent, new_project) # continue up the tree
    if missing_node_name is not None:
        current_node = SubElement(parent_node, missing_node_tag, {'name': missing_node_name})
    else: # parent node did not have a name attribute so this node shouldn't either
        current_node = SubElement(parent_node, missing_node_tag)
    return current_node

def merge_templated_nodes_with_project(templated_nodes, new_project):
    ''' Merge a set of user configured template nodes into a new project.
    
    @param templated_nodes ( [xml_node:Element, ...] ) - list of nodes to merge
    @param new_project (OpusProject) the project in which new nodes are created
    
    Created nodes in the new_project are guaranteed to have the same id-path as in the parent tree of the 
    templated node and thus will overwrite any parents configuration in those places. 
    When the node path doesn't exist in the new project, it is created with empty nodes all the way down to 
    the templated node. This causes the new project to inherit attributes and values from the parent project
    when loaded.
     
    '''
    
    for templated_node in templated_nodes:
        node_id_string = node_identity_string(templated_node)
        
        # try to fetch the existing node in the new project
        node_to_edit = new_project.find_by_id_string(node_id_string)
       
        # create it if it isn't there
        if node_to_edit is None:
            # get a list of all the nodes between the project root and the templated node. This list can then
            # be traversed to figure out which nodes that we need to create in the new project in order for 
            # an inserted node to have the same id-path in the templated project and in the new project 
            nodes_to_parent = []
            walker_node = templated_node.getparent()
            while walker_node.getparent() is not None: # walker.parent == None -> walker is project root
                nodes_to_parent.append(walker_node)
                walker_node = walker_node.getparent()
            del walker_node
            
            # nodes_to_parent.reverse() # we want to traverse from closest parent to furthest
            
            # fetches a reference to the created or existing parent node that we want to attach to            
            node_to_edit_parent_node = _create_or_get_parent(nodes_to_parent, new_project)
            
            # attach the node to the parent
            node_to_edit = SubElement(node_to_edit_parent_node, 
                                       templated_node.tag, 
                                       {'name': templated_node.get('name') or ''})
        
        # copy the text from the templated node to the node in the new project
        node_to_edit.text = templated_node.text

def set_default_project_information(new_project, name, parent):
    pass
