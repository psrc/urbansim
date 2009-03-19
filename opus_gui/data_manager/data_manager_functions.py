# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

'''
A set of functions related to Data Manager and the <data_manager> node
in Opus Project Configuration files.
'''

def get_tool_nodes(project):
    '''
    Retrieve a list of all nodes that represent tools in the given project
    @param project (OpusProject) project to fetch nodes from
    @return a list of nodes representing the tools (list(Element))
    '''
    tool_nodes = []
    tool_group_nodes = [node for node in get_tool_library_node(project) if
                        node.get('type') == 'tool_group']
    for tool_group in tool_group_nodes:
        tool_nodes.extend([node for node in tool_group if 
                           node.get('type') == 'tool_file'])
    return tool_nodes

def get_tool_node_by_name(project, tool_name):
    '''
    Fetch a node representing a tool based in it's name.
    @param project (OpusProject) project to fetch node from
    @param tool_name (str) name of the tool to fetch
    @return the node (Element) or None if the node was not found
    '''
    for node in get_tool_nodes(project):
        if node.tag == tool_name:
            return node
    return None

def get_tool_library_node(project):
    '''
    Get a reference to the tool library for the given project
    @param project (OpusProject) project to operate on
    @return the node representing the tool library (Element) or None if the
    project does not contain a tool library.
    '''
    return project.find('data_manager/Tool_Library')
