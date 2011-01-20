# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

def get_model_nodes(project):
    '''
    Get a list of all model nodes in the project.

    @param project (OpusProject) the project to fetch values from
    @return the list of available model nodes (list(Element))
    '''
    return project.findall('model_manager/models/model')

def get_model_names(project):
    '''
    Get a list of model names in the project.

    @param project (OpusProject) the project to fetch values from
    @return the list of available model nodes (list(Element))
    '''
    return [node.get('name') for node in get_model_nodes(project)]