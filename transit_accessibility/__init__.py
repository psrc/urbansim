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

def __get_version():
    from opus_core.get_version import get_version
    
    try:
        import __from_installer__
        installed = True
    except ImportError:
        installed = False
    
    # The build number in following "build = ..." line is automatically updated 
    # each time Fireman builds this project.
    build = '0'
        
    return get_version(build, installed)
    

__version__ = __get_version()