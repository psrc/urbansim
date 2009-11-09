# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import time
import tempfile

from shutil import rmtree

from opus_core.logger import logger


class SimulationState(object):
    """Singleton for storing information about the state of a simulation.
    Only creates cache directory when get_cache_directory() is called.
    """
    
    class __impl(object):
        """ Implementaion of the singleton """ 
        def __init__(self, 
                current_time, ### TODO: Changes often. Does this belong in a Singleton?
                low_memory_run, ### TODO: This seems like configuration information.
                base_cache_dir, ### TODO: This seems like configuration information.
                time_increment=1, ### TODO: Related to current_time. Does this belong in a Singleton?
                created_base_cache_dir=False ### TODO: Probably eliminate this entirely. Why would SimulationState create a directory???
                ):
            self.current_time = current_time
            self.low_memory_run = low_memory_run
            self.base_cache_dir = base_cache_dir
            self.simulation_start_datetime = time.localtime(time.time())
            cache_dir = os.path.join(self.base_cache_dir,
                                     time.strftime("%y_%m_%d_%H_%M_%S", self.simulation_start_datetime))
            self.set_cache_directory(cache_dir)
            self._created_base_cache_dir = created_base_cache_dir
            self.time_increment = time_increment
                        
        def set_current_time(self, time):
            self.current_time = time

        def get_current_time(self):
            return self.current_time
        
        def get_prior_time(self):
            return self.current_time - self.time_increment
        
        def set_low_memory_run(self, is_low_memory_run):
            self.low_memory_run = is_low_memory_run
            
        def get_low_memory_run(self):
            return self.low_memory_run
        
        def cache_directory_exists(self):
            return os.path.exists(self.cache_directory)
        
        def create_cache_directory(self):
            logger.log_status("Creating cache directory '%s'." % self.cache_directory)
            os.makedirs(self.cache_directory)
        
        ### TODO: Probably get rid of this. Why would SimulationState create a directory???
        def remove_base_cache_directory(self):
            """The cache directory is deleted only if it was created within this class."""
            if self._created_base_cache_dir:
                logger.log_status("Removing cache directory " + self.base_cache_dir)
                try:
                    rmtree(self.base_cache_dir)
                except:
                    pass
            self._created_base_cache_dir = False

        def get_cache_directory(self):

            return self.cache_directory
        
        def set_cache_directory(self, cache_directory):
            self.cache_directory = cache_directory
            
        def get_current_cache_directory(self):
            """Return cache_directory/current_time"""
            return os.path.join(self.get_cache_directory(), str(self.get_current_time()))
        
    __instance = None
    
    def __init__(self, current_year=0, low_memory_run=False, base_cache_dir=None, new_instance=False):
        if new_instance or (base_cache_dir is not None):
            self.remove_singleton()
        if SimulationState.__instance is None:
            
            ### TODO: Probably get rid of this. Why should SimulationState be 
            ###       responsible for creating this directory? Do we think that
            ###       the user is going to remember to delete it??? Does 
            ###       everyone always remember to call remove_singleton after
            ###       they are done using it? I sure hope not, or the Singleton
            ###       would not even function! This is a likely source of many
            ###       undeleted temporary directories.
            if not base_cache_dir:
                base_cache_dir = tempfile.mkdtemp(prefix='opus_core_tmp')
                created_base_cache_dir = True
            else:
                created_base_cache_dir = False
                
            SimulationState.__instance = SimulationState.__impl(current_year, low_memory_run, base_cache_dir,
                                                                created_base_cache_dir=created_base_cache_dir)
    def __getattr__(self, attr):
        """Delegate access to implementation"""
        return getattr(self.__instance, attr)
    
    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
    
    def remove_singleton(self, delete_cache=False):
        """Resets this object so that next call will re-create a new singleton."""
        
        ### TODO: Probably get rid of this. Why is SimulationState creating directories???
        if delete_cache:
            if SimulationState.__instance <> None:
                self.remove_base_cache_directory()
                
        SimulationState.__instance = None
    