# This module collects MTC travel model functionality common to the import,
# export, and travel model invocation components.

import os

def tm_get_base_dir(config):
    tm_config = config['travel_model_configuration']
    tm_home = tm_config['travel_model_home']
    if 'directory' not in tm_home:
        raise KeyError("Cannot find directory for travel model home")

    tm_base_dir = tm_home['directory']

    # Now we must ensure that the directory is mounted if necessary
    if 'proto' not in tm_home:
        return tm_base_dir

    if tm_home['proto'] == 'sshfs':
        connect_string = tm_home['connect_string']
        if os.path.ismount(tm_base_dir) and \
               os.path.exists(os.path.join(tm_base_dir, 'model_support_files')):
            # It appears that to do a more thorough verification here, we'd
            # have to parse /proc/mounts.  This is so platform dependent I
            # didn't bother.
            return tm_base_dir
        cmd = 'sshfs ' + connect_string + ' ' + tm_base_dir
        rc = os.system(cmd)
        if (rc != 0):
            raise IOError("Failed to '" + cmd + "'")
        return tm_base_dir

    else:
        raise NotImplementedError("protocol " + tm_home['proto'] + " is not supported")

def tm_get_data_exchange_dir(config, year):
    tm_config = config['travel_model_configuration']
    base_dir = tm_get_base_dir(config)
    data_exchange_dir = os.path.join(base_dir, tm_config[year]['data_exchange_dir'])
    if not os.path.exists(data_exchange_dir):
        os.makedirs(data_exchange_dir)
    return data_exchange_dir
