#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

# ********** CONSTANTS TO EDIT TO CHANGE VERSION NUMBERS **********

# Edit the following constant to change the major, minor, and bugfix numbers,
# or to change from development to stable releases
# if this is a stable release, change version to include a bugfix number (e.g. '4.2.3'), and stable to True
opus_version = '4.2'
stable = False

# Minumimum and maximum version numbers for XML that this code is guaranteed to work for.
# (It might work for others, but no promises.)
minimum_xml_version = '1.0'
maximum_xml_version = '1.0'

# ********** END OF CONSTANTS TO EDIT TO CHANGE VERSION NUMBERS **********


import sys, re
from subprocess import Popen, PIPE


def get_opus_version_number(package_name='opus_core'):
    """Return a string with the version number for this version of the Opus code.  
    The variable opus_core.__version__ is set to this string (and maybe later in 
    all Opus/UrbanSim packages).  For stable releases, the version is something like 
    '4.2.1', where 4 is the major release number (i.e. UrbanSim 4), 2 is the minor number, 
    and 1 is the bugfix number.  For development versions, the version is something like 
    '4.3-dev3216' where 3216 is the svn revision number for this version.  When this 
    development version is first released as a stable release, it will become '4.3.0'.  
    The svn revision number is found using either the svnversion program (Mac/Linux) or 
    SubWCRev from TortoiseSVN (Windows) -- if the program isn't available or the code is 
    missing the svn information, the version for a development version will be e.g. 
    '4.3-dev (revision number not available)'
    """
    
    if stable:
        return opus_version
    # it's a development version - try to find the svn revision number
    # default phrase for the revision -- override if we can find the real number
    revision = ' (revision number not available)'
    # There are various things that can go wrong with getting the revision number
    # (svn information missing, etc etc).  We don't want to crash just finding the
    # version number, so wrap the whole thing in a try/except block that will catch
    # any exception.  (Normally bad programming practice ...)
    try:
        # locate where opus_core is living
        package_dir = __import__(package_name).__path__[0]
        if sys.platform=='win32':
            # It's a windows machine -- use SubWCRev.  This may not be on the user's search
            # path, so if just calling it doesn't work try guessing where it is.  (This is 
            # where TortoiseSVN installs it by default). 
            try:
                cmd = r'SubWCRev ' + package_dir
                (svn_response, err) = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
            except WindowsError:
                cmd = r'C:\Program Files\TortoiseSVN\bin\SubWCRev ' + package_dir
                (svn_response, err) = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
            if err=='':
                # if no error, the last line of the response will be something like
                # 'Updated to revision 3024', with a newline following -- get the '3024' part
                revision= svn_response.split()[-1]
        else:
            # it's Mac or linux -- use svnversion.  This returns a number if it succeeds, 
            # with an M following if the files have been modified, and with two numbers separated
            # by : for mixed revisions.  Get the last number out of the response, and use that.
            # (So for example if svnversion returns 4123:4168MS, get 4168 as the revision number.)
            cmds = ('svnversion', package_dir)
            (svn_response, err) = Popen(cmds, stdout=PIPE, stderr=PIPE).communicate()
            if err=='':
                ns = re.findall(r'\d+', svn_response)
                if len(ns)>0:
                    revision= ns[-1]
    except:
        pass
    return "%s-dev%s" % (opus_version, revision)
