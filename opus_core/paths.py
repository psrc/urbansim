# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

def get_opus_home_path(*args):
    return os.path.join(OPUS_HOME, *args)

def get_opus_data_path_path(*args):
    return os.path.join(OPUS_DATA_PATH, *args)

def get_settings_path(*args):
    return os.path.join(OPUS_SETTINGS_PATH, *args)

def get_project_configs_path(*args):
    return os.path.join(OPUS_PROJECT_CONFIGS_PATH, *args)

def get_local_databases_path(*args):
    return os.path.join(OPUS_LOCAL_DATABASES_PATH, *args)

def prepend_opus_home_if_relative(path):
    if os.path.isabs(path):
        return path
    return get_opus_home_path(path)

def prepend_opus_data_path_if_relative(path):
    if os.path.isabs(path):
        return path
    return get_opus_data_path_path(path)

def _safe_getenv(key, default_func):
    return os.environ[key] if key in os.environ else default_func()

def _get_default_opus_home():
    raise Exception('OPUS_HOME environment variable must be set.') 

def _get_default_opus_data_path():
    return get_opus_home_path('data') 

OPUS_HOME = _safe_getenv('OPUS_HOME', _get_default_opus_home)
OPUS_DATA_PATH = _safe_getenv('OPUS_DATA_PATH', _get_default_opus_data_path)
OPUS_SETTINGS_PATH = get_opus_home_path('settings')
OPUS_PROJECT_CONFIGS_PATH = get_opus_home_path('project_configs')
OPUS_LOCAL_DATABASES_PATH = get_opus_home_path('local_databases')
