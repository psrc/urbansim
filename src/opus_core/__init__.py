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

def __get_version(build_id, installed):
    """
    Returns the major.minor.build version for the given package and build_id.
    """

    ############################################################################

    major = '4'
    minor = '1'
    
    ############################################################################
        
    if installed:
        cvs = ''
    else:
        cvs = ' (from cvs)'
    
    return '%s.%s.%s%s' % (major, minor, build_id, cvs)
    
def __get_build():
    # The build number in following "build = ..." line is automatically updated 
    # each time Fireman builds this project.
    build = '0964'
    
    return build
    
def __is_installed():
    import os
    
    try:
        import __from_installer__
        return True
    except:
        return False


__version__ = __get_version(__get_build(), __is_installed())