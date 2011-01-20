# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
import os

def get_builtin_project_templates():
    '''
    Returns a dictionary of projects to show up in the 'Load project template' dialog.
    Each entry has the title of the template as the key and the absolute path to the project template file as
    value.

    '''
    opus_core_dir = __import__('opus_core').__path__[0]
    workspace_dir = os.path.split(opus_core_dir)[0]
    
    
    # TODO replace the bare projects with fleshed out template projects that could actually work on their own
    # when inherited directly
    
    builtin_project_templates = {
    'Gridcell Template': os.path.join(workspace_dir, 'urbansim_gridcell', 'configs', 'urbansim_gridcell.xml'),
    'Parcel Template': os.path.join(workspace_dir, 'urbansim_parcel', 'configs', 'urbansim_parcel.xml'),
    'Zone Template': os.path.join(workspace_dir, 'urbansim_zone', 'configs', 'urbansim_zone.xml')
    }
    
    return builtin_project_templates