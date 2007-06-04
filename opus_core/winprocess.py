#
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

from win32process import GetCurrentProcessId, GetProcessMemoryInfo
from win32con import PROCESS_QUERY_INFORMATION, PROCESS_SET_INFORMATION, PROCESS_ALL_ACCESS
from win32api import OpenProcess

class WinProcess(object):
    """ A Singleton class to print the memory usage of current process.
        Call current_process_memory_info will return a tuple of (pid, mem)        
        
        Note that the functions used in this class only work under
        Windows platform and with Python version at least 2.4 installed.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def current_process_memory_info(self):
        """Return memory_info in KB of current process """
        try:
            process = self._current_process()
            process_handle = OpenProcess(PROCESS_QUERY_INFORMATION, 0, process)
            return self._get_process_memory_info(process, process_handle)
        except:
            return None

    def _get_process_memory_info(self, process, process_handle):
        if process != None and process_handle != None:
            process_memory_info = self._get_memory_info(process_handle)
            process_memory_usage = (process_memory_info["WorkingSetSize"]/1024)
            #print "PID: %s Mem: %sK" % (process, process_memory_usage)
            return (process, process_memory_usage)

    def _current_process(self):
        return GetCurrentProcessId()
    
    def _get_memory_info(self, process_handle):
        return GetProcessMemoryInfo(process_handle)


